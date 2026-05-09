import hashlib
import json
import sqlite3
import time
from datetime import datetime, timezone

import httpx

from config import (
    ANTHROPIC_API_KEY, MODEL, DB_PATH, PROMPTS_PATH, MAX_TOKENS, TIMEOUT,
)


def call_anthropic(prompt_text):
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
                "messages": [{"role": "user", "content": prompt_text}],
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

    return {
        "elapsed_ms": elapsed_ms,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "output_text": output_text,
        "output_hash": output_hash,
        "error": error,
    }


def main():
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY is empty. Set it in .env")

    with open(PROMPTS_PATH) as f:
        prompts = [json.loads(line) for line in f if line.strip()]

    if not prompts:
        raise RuntimeError(f"No prompts found in {PROMPTS_PATH}")

    conn = sqlite3.connect(DB_PATH)
    n_errors = 0
    sum_elapsed = 0.0
    sum_in = 0
    sum_out = 0
    last_ts = None

    for prompt in prompts:
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        last_ts = ts
        result = call_anthropic(prompt["text"])

        conn.execute(
            """
            INSERT INTO observations
            (ts, provider, model, prompt_id, elapsed_ms,
             input_tokens, output_tokens, output_text, output_hash, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (ts, "anthropic", MODEL, prompt["id"], result["elapsed_ms"],
             result["input_tokens"], result["output_tokens"],
             result["output_text"], result["output_hash"], result["error"]),
        )
        conn.commit()

        if result["error"]:
            n_errors += 1
        else:
            sum_elapsed += result["elapsed_ms"]
            sum_in += result["input_tokens"] or 0
            sum_out += result["output_tokens"] or 0

    row_count = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
    conn.close()

    print(f"ts:              {last_ts}")
    print(f"prompts:         {len(prompts)}")
    print(f"errors:          {n_errors}/{len(prompts)}")
    print(f"elapsed_ms_sum:  {sum_elapsed:.1f}")
    print(f"tokens (in/out): {sum_in} / {sum_out}")
    print(f"total_rows:      {row_count}")


if __name__ == "__main__":
    main()
