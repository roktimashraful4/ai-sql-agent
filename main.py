from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from agent import chain
from db import get_schema, run_safe_query
import logging

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- Utility functions ---
def clean_sql(output: str) -> str:
    return output.replace("```sql", "").replace("```", "").strip()

def is_query_safe(query: str) -> bool:
    q = query.strip().lower()
    return (
        q.startswith("select")
        and all(bad not in q for bad in ["insert", "update", "delete", "drop", "alter", "truncate"])
    )

# --- Routes ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    schema = get_schema()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "schema": schema
    })

@app.post("/query", response_class=HTMLResponse)
async def query_handler(request: Request, query: str = Form(...)):
    schema = get_schema()
    try:
        # Run agent and clean output
        raw_output = await chain.ainvoke({"schema": schema, "question": query})
        sql_query = clean_sql(raw_output)

        # Validate safety
        if not is_query_safe(sql_query):
            return templates.TemplateResponse("index.html", {
                "request": request,
                "query": sql_query,
                "error": "Unsafe query detected. Only SELECT statements are allowed.",
                "schema": schema
            })

        # Run SQL
        records = run_safe_query(sql_query)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "query": sql_query,
            "records": records,
            "schema": schema
        })

    except Exception as e:
        logging.exception("Error handling query")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Failed to process your request: {str(e)}",
            "schema": schema
        })
