import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Load OpenRouter API Key
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("Missing OPENROUTER_API_KEY in .env")

# Initialize the model
llm = ChatOpenAI(
    temperature=0,
    model="deepseek/deepseek-r1:free",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=api_key,
)

# Improved prompt: explicitly tell the model to refuse harmful commands
prompt = PromptTemplate.from_template("""\
You are a MySQL expert assistant.
Your job is to convert natural language into valid, plain SQL SELECT statements ONLY.
- Only return SELECT queries.
- NEVER generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, or any harmful commands.
- If the user requests any harmful or non-SELECT SQL, respond only with the exact message:
"Agent cannot perform that operation."
- Do NOT include markdown in your response.
- Do NOT explain anything.

Schema:
{schema}

Question:
{question}

SQL Query:
""")

# Chain prompt -> model -> output parser
chain = RunnableSequence(
    prompt | llm | StrOutputParser()
)

# Dangerous keywords list for quick check
DANGEROUS_KEYWORDS = ["drop", "delete", "update", "insert", "alter", "truncate"]

def contains_dangerous_command(text: str) -> bool:
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in DANGEROUS_KEYWORDS)

def clean_sql(output: str) -> str:
    # Remove any markdown and trim spaces
    return output.replace("```sql", "").replace("```", "").strip()

def is_query_safe(query: str) -> bool:
    q = query.strip().lower()
    # Check if it starts with SELECT and does NOT contain dangerous keywords
    return (
        q.startswith("select") and
        all(bad not in q for bad in DANGEROUS_KEYWORDS)
    )

def generate_sql(schema: str, question: str) -> str:
    # 1. Pre-check question for dangerous keywords
    if contains_dangerous_command(question):
        return "Agent cannot perform that operation."

    # 2. Call the LLM chain
    sql_output = chain.invoke({"schema": schema, "question": question})
    sql_clean = clean_sql(sql_output).lower()

    # 3. Check if the output is the explicit denial message from the model
    if sql_clean == "agent cannot perform that operation.":
        return sql_clean

    # 4. Validate the output SQL for safety
    if not is_query_safe(sql_clean):
        return "Agent cannot perform that operation."

    # 5. Additional check for suspicious fallback queries like "WHERE 1 = 0"
    if "where 1 = 0" in sql_clean:
        return "Agent cannot perform that operation."

    # 6. Return safe SQL
    return sql_clean