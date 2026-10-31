CREATE TABLE IF NOT EXISTS conversations (
    id         SERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    status     VARCHAR(10) NOT NULL DEFAULT 'bot'
               CHECK (status IN ('bot', 'human', 'closed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
