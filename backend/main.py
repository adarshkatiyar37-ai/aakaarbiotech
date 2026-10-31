import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(title="Help Desk")


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
