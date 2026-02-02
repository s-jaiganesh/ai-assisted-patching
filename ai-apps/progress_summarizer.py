import argparse
from .db_reader import fetch_summary, fetch_failures
from .prompts import build_progress_prompt, SYSTEM_PROMPT_STATUS
from .gas_llm_client import call_company_llm
from .teams_notifier import send_teams


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--change-id", required=True)
    ap.add_argument("--table", help="DB table name (e.g. patch_status_20260131_163427)")
    ap.add_argument("--failures-limit", type=int, default=20)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--dry-run", action="store_true", help="Print instead of posting to Teams")
    ap.add_argument("--simulate", action="store_true", help="No DB. Uses fake data to test AI + output.")
    args = ap.parse_args()

    if args.simulate:
        stats = {"total": 5, "pre_reboot_ok": 4, "pre_reboot_fail": 1, "apply_patch_ok": 3, "apply_patch_fail": 1}
        failures = [{"server": "host3", "apply_patch": "failed", "apply_patch_summary": "Disk space low on /boot"}]
    else:
        if not args.table:
            raise SystemExit("Missing --table (or use --simulate).")
        stats = fetch_summary(args.table)
        failures = fetch_failures(args.table, limit=args.failures_limit)

    prompt = build_progress_prompt(args.change_id, stats, failures)
    msg = call_company_llm(prompt=prompt, system_prompt=SYSTEM_PROMPT_STATUS, temperature=args.temperature)

    send_teams(msg, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
