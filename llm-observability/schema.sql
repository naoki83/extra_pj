CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt_id TEXT NOT NULL,
    elapsed_ms REAL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    output_text TEXT,
    output_hash TEXT,
    error TEXT
);
