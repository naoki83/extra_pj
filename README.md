# extra_pj

Low-cost AI tooling and automation experiments.

## Status

Early / experimental. Public for transparency, not for marketing.

## Current project

**[llm-observability](llm-observability/)** — a minimal append-only runner
that measures Anthropic API behavior (latency, tokens, output) on a fixed
prompt at hourly cadence. Single Python script, SQLite, no dashboard.

See [`llm-observability/README.md`](llm-observability/README.md) for what
it does, what it doesn't, and how to reproduce it in 10 minutes.

## What this is not

- not a SaaS
- not a dashboard
- not a trading bot
- not investment advice

## Layout

```
extra_pj/
├── COMPOUND_SYSTEM_ARCHITECTURE.md   # long-term scope and anti-patterns
├── PRODUCT_V1.md                     # current product scope (frozen)
└── llm-observability/                # current project source
```

## License

Per-project. See each subdirectory.
