import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = "claude-haiku-4-5"
DB_PATH = str(ROOT / "data" / "observations.db")
PROMPTS_PATH = str(ROOT / "prompts" / "v0.jsonl")
MAX_TOKENS = 512
TIMEOUT = 60
