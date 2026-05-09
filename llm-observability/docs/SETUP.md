# SETUP

10 minutes from `git clone` to first row in DB, plus scheduling.

## Prerequisites (not counted in the 10 minutes)

- Python 3.10 or later (`python --version`)
- An Anthropic API key (https://console.anthropic.com)
- A terminal (PowerShell on Windows, Terminal on macOS/Linux)
- `git` installed

## 1. Clone the repo

```cmd
git clone <repo-url>
cd llm-observability
```

## 2. Create a virtual environment

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks the script, run once:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows (cmd)

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```
pip install -r requirements.txt
```

This installs only `httpx` and `python-dotenv`. No heavy frameworks.

## 4. Set the API key

### Windows

```cmd
copy .env.example .env
notepad .env
```

### macOS / Linux

```bash
cp .env.example .env
$EDITOR .env
```

Replace `sk-ant-xxxxxxxxxxxx` with your actual Anthropic API key. Save.

## 5. Initialize the database

From the project root:

```
python -c "import os; os.makedirs('data', exist_ok=True); import sqlite3; sqlite3.connect('data/observations.db').executescript(open('schema.sql').read())"
```

This creates `data/observations.db` with the `observations` table.
Safe to run multiple times.

## 6. First manual run

```
cd src
python observability.py
```

Expected output:

```
ts:             2026-05-07T14:32:18+00:00
elapsed_ms:     1428.31
input_tokens:   168
output_tokens:  82
output_hash:    a3f1b9c4e2d57081
error:          None
total_rows:     1
```

If `error: None` and `total_rows: 1` (or higher if you ran more than
once), the runner works.

## 7. Schedule hourly runs

### Windows: Task Scheduler

1. Open **Task Scheduler** (`taskschd.msc`).
2. **Create Task** (not "Create Basic Task" — you need full options).
3. **General** tab:
   - Name: `llm-observability`
   - "Run whether user is logged on or not" (optional, but recommended)
4. **Triggers** tab → **New**:
   - Begin the task: **On a schedule**
   - Daily, recur every 1 day
   - **Advanced**: Repeat task every **1 hour**, for a duration of **1 day**
   - Enabled
5. **Actions** tab → **New**:
   - Action: **Start a program**
   - Program/script: full path to `.venv\Scripts\python.exe`
     (e.g. `C:\Users\YOU\llm-observability\.venv\Scripts\python.exe`)
   - Add arguments: `src\observability.py`
   - Start in: full path to the `llm-observability` directory
     (e.g. `C:\Users\YOU\llm-observability`)
6. **Conditions** tab:
   - Uncheck "Start the task only if the computer is on AC power"
     (if you're on a laptop and want runs to continue on battery)
7. OK. Enter your Windows password if prompted.

To confirm: right-click the task → **Run**. Then check the DB (Section 8).

### macOS / Linux: cron

```bash
crontab -e
```

Add (adjust the path):
```
17 * * * * cd /full/path/to/llm-observability && .venv/bin/python src/observability.py >> logs/cron.log 2>&1
```

Minute `:17` avoids common `:00` traffic spikes. Create `logs/`:
```bash
mkdir -p logs
```

## 8. Verify the runner is being scheduled

After 24+ hours of scheduling:

```
sqlite3 data/observations.db "SELECT COUNT(*) FROM observations"
```

Should return roughly 24 (give or take depending on when you started).

```
sqlite3 data/observations.db "SELECT ts, elapsed_ms, output_tokens, error FROM observations ORDER BY id DESC LIMIT 10"
```

All recent rows should have `error` empty (NULL). `elapsed_ms` typically
1500–3500. `output_tokens` typically 40–120 (varies with model behavior).

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `RuntimeError: ANTHROPIC_API_KEY is empty` | `.env` missing or key not set | Re-check Section 4 |
| `httpx.HTTPStatusError` 401 | invalid API key | Generate a new one |
| `httpx.HTTPStatusError` 429 | rate limit hit | Lower run frequency, or wait |
| `httpx.HTTPStatusError` 529 | provider overloaded | Transient, will recover |
| Row count not increasing after 24h | scheduler not running | Check Task Scheduler history / `cron.log` |
| Task Scheduler runs but no row | wrong "Start in" path or venv path | Re-check absolute paths in Section 7 |
| `python: command not found` (cron) | cron has no PATH | Use absolute path to `.venv/bin/python` |

## What "10 minutes" actually means

Sections 1–6 (clone through first manual run) on a machine with the
prerequisites met: typically 8–12 minutes including reading.
Section 7 (scheduling) adds 3–5 minutes. Section 8 (verify) requires
24 hours of elapsed time.

## What's not in this guide

- Multi-provider setup (out of scope)
- Anomaly detection (out of scope)
- Dashboard / visualization (intentionally not provided)
- CI / Docker / cloud deployment (community contributions welcome,
  not maintained by the operator)
