#!/usr/bin/env python3
import argparse, os
from ai_client import call_company_llm
from teams_notifier import send_teams
from db_reader import fetch_summary, fetch_failures
from prompts import build_progress_prompt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--change-id", default=os.environ.get("CHANGE_ID","UNKNOWN"))
    ap.add_argument("--table", default=os.environ.get("PATCH_TABLE","patch_status"))
    ap.add_argument("--failures-limit", type=int, default=20)
    ap.add_argument("--temperature", type=float, default=0.2)
    args = ap.parse_args()

    stats = fetch_summary(args.table)
    failures = fetch_failures(args.table, limit=args.failures_limit)

    prompt = build_progress_prompt(args.change_id, stats, failures)
    msg = call_company_llm(prompt, temperature=args.temperature)
    send_teams(msg)

if __name__ == "__main__":
    main()
