CREATE TABLE IF NOT EXISTS messages (
    id              SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL
                    REFERENCES conversations(id) ON DELETE CASCADE,
    sender          VARCHAR(10) NOT NULL
                    CHECK (sender IN ('customer', 'bot', 'admin')),
    text            TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
