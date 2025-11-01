from fastapi import FastAPI
from pydantic import BaseModel
import duckdb
import re

app = FastAPI()
DB_FILE = 'samarth.duckdb'

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    conn = duckdb.connect(DB_FILE)
    text = q.question.lower()
    match = re.search(r"rainfall in (.+) and (.+) for the last (\d+)", text)
    if not match:
        return {"error": "Use this format: Compare rainfall in State1 and State2 for the last N years."}

    s1, s2, n = match.groups()
    n = int(n)

    q1 = f"SELECT state, AVG(rainfall_mm) AS avg_rain FROM rainfall WHERE state ILIKE '%{s1.strip()}%' GROUP BY state"
    q2 = f"SELECT state, AVG(rainfall_mm) AS avg_rain FROM rainfall WHERE state ILIKE '%{s2.strip()}%' GROUP BY state"

    try:
        r1 = conn.execute(q1).fetchdf()
        r2 = conn.execute(q2).fetchdf()
        return {
            "question": q.question,
            "result": [
                {"state": s1.title(), "avg_rainfall": float(r1['avg_rain'][0])},
                {"state": s2.title(), "avg_rainfall": float(r2['avg_rain'][0])}
            ],
            "source": [
                "https://www.data.gov.in/resource/sub-divisional-monthly-rainfall-1901-2017"
            ]
        }
    except Exception as e:
        return {"error": str(e)}
