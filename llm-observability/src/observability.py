import hashlib
import json
import sqlite3
import time
from datetime import datetime, timezone

import httpx

from config import (
    ANTHROPIC_API_KEY, MODEL, DB_PATH, PROMPTS_PATH, MAX_TOKENS, TIMEOUT,
)


def main():
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY is empty. Set it in .env")

    with open(PROMPTS_PATH) as f:
        prompt = json.loads(f.readline())

    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    error = None
    elapsed_ms = None
    input_tokens = None
    output_tokens = None
    output_text = None
    output_hash = None

    t0 = time.perf_counter()
    try:
        r = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": MODEL,
                "max_tokens": MAX_TOKENS,
                "messages": [{"role": "user", "content": prompt["text"]}],
            },
            timeout=TIMEOUT,
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000
        r.raise_for_status()
        data = r.json()
        input_tokens = data["usage"]["input_tokens"]
        output_tokens = data["usage"]["output_tokens"]
        output_text = data["content"][0]["text"]
        output_hash = hashlib.sha256(output_text.encode()).hexdigest()[:16]
    except Exception as e:
        if elapsed_ms is None:
            elapsed_ms = (time.perf_counter() - t0) * 1000
        error = f"{type(e).__name__}: {e}"

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        INSERT INTO observations
        (ts, provider, model, prompt_id, elapsed_ms,
         input_tokens, output_tokens, output_text, output_hash, error)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (ts, "anthropic", MODEL, prompt["id"], elapsed_ms,
         input_tokens, output_tokens, output_text, output_hash, error),
    )
    conn.commit()

    row_count = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
    last = conn.execute(
        "SELECT ts, elapsed_ms, input_tokens, output_tokens, output_hash, error "
        "FROM observations ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.close()

    print(f"ts:             {last[0]}")
    print(f"elapsed_ms:     {last[1]}")
    print(f"input_tokens:   {last[2]}")
    print(f"output_tokens:  {last[3]}")
    print(f"output_hash:    {last[4]}")
    print(f"error:          {last[5]}")
    print(f"total_rows:     {row_count}")


if __name__ == "__main__":
    main()
