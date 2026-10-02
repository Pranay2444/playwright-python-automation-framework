"""Day 1: keep environment values in one place, outside test functions."""

import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
# Existing environment variables win over the local .env file, including in CI.
load_dotenv(PROJECT_ROOT / ".env", override=False)

BASE_URL = os.getenv("BASE_URL", "https://practicesoftwaretesting.com").rstrip("/")
API_BASE_URL = os.getenv(
    "API_BASE_URL", "https://api.practicesoftwaretesting.com"
).rstrip("/")
PW_PROXY_SERVER = os.getenv("PW_PROXY_SERVER") or None
REQUEST_TIMEOUT_MS = int(os.getenv("REQUEST_TIMEOUT_MS", "30000"))
if REQUEST_TIMEOUT_MS <= 0:
    raise ValueError("REQUEST_TIMEOUT_MS must be a positive integer")
