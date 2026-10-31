CREATE TABLE IF NOT EXISTS kb_articles (
    id      SERIAL PRIMARY KEY,
    title   VARCHAR(200) NOT NULL,
    content TEXT NOT NULL
);
