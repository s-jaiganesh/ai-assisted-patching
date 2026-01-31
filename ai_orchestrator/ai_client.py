import os, requests

def call_company_llm(prompt: str, temperature: float = 0.2) -> str:
    url = os.environ.get("COMPANY_LLM_URL")
    token = os.environ.get("COMPANY_LLM_TOKEN")
    if not url or not token:
        raise RuntimeError("Missing COMPANY_LLM_URL or COMPANY_LLM_TOKEN")
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json", "Accept":"application/json"}
    r = requests.post(url, headers=headers, json={"prompt": prompt, "temperature": temperature}, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data.get("response") or data.get("output") or str(data)
