import requests
from .config import TEAMS_WEBHOOK


def send_teams(message: str, dry_run: bool = False) -> None:
    # If webhook not ready, just print (your requested test mode)
    if dry_run or not TEAMS_WEBHOOK:
        print("\n===== TEAMS MESSAGE (PRINT MODE) =====\n")
        print(message)
        print("\n===== END =====\n")
        return

    r = requests.post(TEAMS_WEBHOOK, json={"text": message}, timeout=10)
    r.raise_for_status()
