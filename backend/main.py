import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI
from groq import Groq
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Help Desk")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-20b"


class ChatRequest(BaseModel):
    message: str


def get_connection():
    return psycopg.connect(os.getenv("DATABASE_URL"))


@app.get("/")
def home():
    return {"message": "Help desk chal raha hai"}


@app.get("/articles")
def list_articles():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, content FROM kb_articles ORDER BY id")
            rows = cur.fetchall()
    return [
        {"id": r[0], "title": r[1], "content": r[2]}
        for r in rows
    ]


@app.get("/articles/search")
def search_articles(q: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, content FROM kb_articles "
                "WHERE title ILIKE %s OR content ILIKE %s ORDER BY id",
                (f"%{q}%", f"%{q}%"),
            )
            rows = cur.fetchall()
    return [
        {"id": r[0], "title": r[1], "content": r[2]}
        for r in rows
    ]


@app.post("/chat")
def chat(req: ChatRequest):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT title, content FROM kb_articles ORDER BY id")
            rows = cur.fetchall()

    faq_text = "\n".join(f"- {title}: {content}" for title, content in rows)

    system_prompt = (
        "Tum ek help desk assistant ho. Hinglish me chhote aur saaf jawab do. "
        "Sirf neeche di gayi FAQ ke hisaab se jawab do. "
        "Agar jawab FAQ me nahi hai, to saaf bolo ki tumhe nahi pata, "
        "aur kaho ki abhi tum is sawal ka jawab nahi de sakte, customer office se seedha sampark kare. Kabhi mat kehna ki request note ya save ho gayi hai. "
        "Kabhi andaza mat lagao.\n\nFAQ:\n" + faq_text
    )

    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.message},
        ],
    )
    return {"reply": response.choices[0].message.content}
