import os

# --- GAS / Apigee environment ---
GAS_ENV = os.getenv("GAS_ENV", "st")
GAS_CLIENT_ID = os.getenv("GAS_CLIENT_ID")
GAS_CLIENT_SECRET = os.getenv("GAS_CLIENT_SECRET")
GAS_MODEL = os.getenv("GAS_MODEL")  # e.g. your internal model name
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))

APIGEE_BASE_URL = f"https://{GAS_ENV}.api.genpt.com"
TOKEN_URL = f"{APIGEE_BASE_URL}/oauthv2/token"
LLM_PROXY_URL = f"{APIGEE_BASE_URL}/genaisp/gas"

# --- DB (optional for testing AI part; you can also use --simulate) ---
PATCH_DB_HOST = os.getenv("PATCH_DB_HOST")
PATCH_DB_PORT = int(os.getenv("PATCH_DB_PORT", "5432"))
PATCH_DB_NAME = os.getenv("PATCH_DB_NAME", "patching")
PATCH_DB_USER = os.getenv("PATCH_DB_USER")
PATCH_DB_PASSWORD = os.getenv("PATCH_DB_PASSWORD")

# --- Teams (optional; if missing, we just print) ---
TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK")


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
        raise RuntimeError(f"Missing env vars: {', '.join(missing)}")
