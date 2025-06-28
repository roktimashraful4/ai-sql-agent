# 🧠 AI-Powered MySQL Query Assistant

![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-AI-blueviolet?logo=python)
![OpenRouter](https://img.shields.io/badge/OpenRouter-GPT--4-blue?logo=openai)
![License](https://img.shields.io/badge/license-MIT-lightgrey)


This project is an AI-powered SQL assistant that allows users to ask natural language questions and receive safe, executable SQL queries with results from their own database.

---

## ⚙️ Tech Stack
- **Frontend:** HTML + TailwindCSS + JavaScript (AJAX)
- **Backend:** FastAPI (Python)
- **LLM API:** OpenRouter (DeepSeek / GPT / Claude etc.)
- **LangChain:** For prompt chaining and LLM invocation

---

## 🚀 Features
- Type questions like “Show all users” or “Users who have due invoice”
- Safe SQL generation (SELECT only)
- Live schema preview in sidebar (Tree View)
- Smooth query UI with typing effect and instant results

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/roktimashraful4/ai-sql-agent.git
cd sql-assistant
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up `.env` file
Create a `.env` file with your OpenRouter API key:
```
DB_HOST=localhost
DB_USER=
DB_PASS=
DB_NAME=
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 5. Run the application
```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000` in your browser.

---

## 📁 Project Structure
```
├── agent.py              # LLM prompt + chain setup
├── db.py                 # DB schema reader + query runner
├── main.py               # FastAPI app
├── templates/
│   └── index.html        # UI layout and schema/response view
├── static/               # Tailwind JS (CDN used here)
├── .env
└── requirements.txt
```

---

## ✅ Notes
- Only SELECT queries are allowed. Destructive queries are blocked.
- AJAX form submission ensures smooth UX with typing effect.
- Schema rendering is live from your database connection.

---

## 🧠 Model Info
Uses OpenRouter's free models (e.g., `deepseek/deepseek-r1:free`). For better performance, use faster models like:
- `gpt-3.5-turbo`
- `claude-3-sonnet`
- `mistral-7b-instruct`

---

## 📃 License
MIT License – feel free to modify and use it in your own projects.