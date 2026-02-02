import json
from pathlib import Path

# Load secrets from local file (preferred for POC)
_SECRETS_PATH = Path(__file__).with_name("secrets.json")

if not _SECRETS_PATH.exists():
    raise RuntimeError(f"Missing secrets file: {_SECRETS_PATH}. Create it (and gitignore it).")

_secrets = json.loads(_SECRETS_PATH.read_text(encoding="utf-8"))

# --- GAS / Apigee environment ---
GAS_ENV = _secrets.get("GAS_ENV", "st")
GAS_CLIENT_ID = _secrets.get("GAS_CLIENT_ID")
GAS_CLIENT_SECRET = _secrets.get("GAS_CLIENT_SECRET")
GAS_MODEL = _secrets.get("GAS_MODEL")
LLM_TIMEOUT = int(_secrets.get("LLM_TIMEOUT", 60))

APIGEE_BASE_URL = f"https://{GAS_ENV}.api.genpt.com"
TOKEN_URL = f"{APIGEE_BASE_URL}/oauthv2/token"
LLM_PROXY_URL = f"{APIGEE_BASE_URL}/genaisp/gas"

# --- DB ---
PATCH_DB_HOST = _secrets.get("PATCH_DB_HOST")
PATCH_DB_PORT = int(_secrets.get("PATCH_DB_PORT", 5432))
PATCH_DB_NAME = _secrets.get("PATCH_DB_NAME", "patching")
PATCH_DB_USER = _secrets.get("PATCH_DB_USER")
PATCH_DB_PASSWORD = _secrets.get("PATCH_DB_PASSWORD")

# --- Teams ---
TEAMS_WEBHOOK = _secrets.get("TEAMS_WEBHOOK", "")


def require_gas_env():
    missing = []
    for k, v in {
        "GAS_CLIENT_ID": GAS_CLIENT_ID,
        "GAS_CLIENT_SECRET": GAS_CLIENT_SECRET,
        "GAS_MODEL": GAS_MODEL,
    }.items():
        if not v:
            missing.append(k)
    if missing:
        raise RuntimeError(f"Missing config values in secrets.json: {', '.join(missing)}")
