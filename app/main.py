from fastapi import FastAPI
import pandas as pd
from pathlib import Path
from app.query_engine import answer_query
from app.anomaly_detector import detect_anomalies
from app.llm_services import generate_llm_answer
app = FastAPI(title="Support Ticket AI")

# Load CSV file
DATA_PATH = Path(__file__).parent.parent / "data" / "support_tickets.csv"

df = pd.read_csv(DATA_PATH)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Convert numeric columns
for column in ["response_time_hrs", "resolution_time_hrs"]:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "total_tickets": len(df)
    }
@app.get("/anomalies")
def anomalies():
    results = detect_anomalies(df)
    return {
        "total_anomalies": len(results),
        "anomalies": results
    }

@app.get("/query")
def query(question: str):
    # Try local dataset analysis first
    local_answer = answer_query(question, df)

    if not local_answer.startswith("I can answer questions"):
        return {"answer": local_answer}

    # Use Gemini only for questions that need LLM reasoning
    answer = generate_llm_answer(question, df)
    return {"answer": answer}
