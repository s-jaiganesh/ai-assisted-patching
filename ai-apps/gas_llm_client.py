import time
import requests
import litellm
from .config import (
    GAS_CLIENT_ID,
    GAS_CLIENT_SECRET,
    GAS_MODEL,
    TOKEN_URL,
    LLM_PROXY_URL,
    LLM_TIMEOUT,
    require_gas_env,
)

_token_cache = {"token": None, "expires_at": 0}


def _get_access_token() -> str:
    require_gas_env()

    now = time.time()
    if _token_cache["token"] and now < _token_cache["expires_at"]:
        return _token_cache["token"]

    payload = {
        "grant_type": "client_credentials",
        "client_id": GAS_CLIENT_ID,
        "client_secret": GAS_CLIENT_SECRET,
    }

    r = requests.post(TOKEN_URL, data=payload, timeout=30)
    r.raise_for_status()
    data = r.json()

    _token_cache["token"] = data["access_token"]
    _token_cache["expires_at"] = now + int(data.get("expires_in", 3600)) - 60
    return _token_cache["token"]


def call_company_llm(prompt: str, system_prompt: str, temperature: float = 0.2) -> str:
    """
    Calls GAS proxy using litellm (same pattern as your llm_client.py)
    """
    token = _get_access_token()

    resp = litellm.completion(
        model=f"openai/{GAS_MODEL}",
        api_base=LLM_PROXY_URL,
        api_key=token,
        timeout=LLM_TIMEOUT,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content
