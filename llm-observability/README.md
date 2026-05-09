# llm-observability

A minimal, append-only runner that measures LLM provider behavior from the
outside. One Python script, one cron, one SQLite file. No dashboard, no
SaaS, no surprises.

## What it does

Calls the Anthropic API on a fixed prompt at a regular interval (hourly via
cron / Task Scheduler) and records:

- `ts` (UTC, second precision)
- `provider`, `model`, `prompt_id`
- `elapsed_ms` (wall-clock latency including network)
- `input_tokens`, `output_tokens` (provider-reported)
- `output_text` and `output_hash` (sha256, first 16 hex)
- `error` (exception type and message, or NULL)

Each call is one row. Append-only. The point is the time series.

## What it doesn't do

- No dashboard, no UI
- No alerting, no notifications
- No real-time anything
- No multi-provider orchestration *(current build: Anthropic only)*
- No prompt sweeping *(1 fixed prompt, intentionally)*
- No analytics layer
- No SaaS, no hosted version, no auth

If any of the above is what you need, this is not the tool.

## Why

Most LLM observability tools are SaaS or require integration into your
application traffic. This tool measures the **provider** from the outside,
on a fixed prompt, with the rigor you'd apply to a market data feed:
deterministic schedule, explicit storage, full reproducibility.

Output drift, latency degradation, and token-counting changes become
visible if you keep the time series long enough.

## Status

- Version: `v0.1.0-pre` (pre-release; product polish underway)
- Provider: Anthropic
- Model: `claude-haiku-4-5`
- Prompts: 1 (`summarize_v1`)
- Storage: SQLite, single file, append-only
- Schedule: hourly (cron / Task Scheduler), operator-managed
- LOC: ~100 (excluding schema and prompt)

## Cost

Approximately **$0.05–$0.15 per day** in Anthropic API charges at hourly
cadence with the default prompt. Verify against current Anthropic pricing.

## Quickstart

See [docs/SETUP.md](docs/SETUP.md) for the full 10-minute walkthrough
(Windows-first, macOS / Linux notes included).

```bash
git clone <repo-url>
cd llm-observability
python -m venv .venv
# activate venv (see SETUP.md for your platform)
pip install -r requirements.txt
cp .env.example .env       # macOS/Linux, then edit ANTHROPIC_API_KEY
# Windows: copy .env.example .env
python -c "import os; os.makedirs('data', exist_ok=True); import sqlite3; sqlite3.connect('data/observations.db').executescript(open('schema.sql').read())"
cd src
python observability.py
```

A successful first run prints a summary and inserts one row.

## Verifying continuity

After scheduling hourly runs, count rows after 24 hours:

```bash
sqlite3 data/observations.db "SELECT COUNT(*) FROM observations"
sqlite3 data/observations.db "SELECT ts, elapsed_ms, output_tokens, error FROM observations ORDER BY id DESC LIMIT 5"
```

Should be roughly 24 rows after a full day, all with `error` NULL.

## File layout

```
llm-observability/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── schema.sql
├── prompts/
│   └── v0.jsonl              # the one fixed prompt
├── src/
│   ├── config.py
│   └── observability.py      # the runner
└── docs/
    └── SETUP.md              # step-by-step
```

`data/` is created at runtime and gitignored. Sample data is **not**
distributed in this repo; you generate your own by running.

## Philosophy

- continuity over features
- append-only over migrations
- one provider, one prompt, one schedule (initial scope)
- reproducibility over polish
- silence over dashboards

## Roadmap

Future versions may extend the prompt set and add OpenAI / Google as
additional providers. Current focus: maintain the Anthropic time series
and ship as a packaged product.

## License

MIT — see [LICENSE](LICENSE).
