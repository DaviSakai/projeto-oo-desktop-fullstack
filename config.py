# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

USERS_JSON = DATA_DIR / "users.json"
SESSIONS_JSON = DATA_DIR / "sessions.json"

# Hash de senha (PBKDF2)
HASH_NAME = "sha256"
HASH_ITER = 390000
SALT_BYTES = 16

# Segredo para assinar sessões (troque por algo próprio)
SESSION_SECRET = "dev-secret-change-me"
