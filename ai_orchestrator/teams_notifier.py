import os, requests

def send_teams(message: str) -> None:
    hook = os.environ.get("TEAMS_WEBHOOK")
    if not hook:
        raise RuntimeError("Missing TEAMS_WEBHOOK")
    r = requests.post(hook, json={"text": message}, timeout=15)
    r.raise_for_status()
