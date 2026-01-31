#!/usr/bin/env python3
import argparse, json, os, sys, time
import requests

TERMINAL = {"successful","failed","error","canceled"}

def req_env(k):
    v = os.environ.get(k)
    if not v:
        print(f"Missing env var: {k}", file=sys.stderr)
        sys.exit(2)
    return v

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", required=True)
    ap.add_argument("--extra-vars", default="{}")
    ap.add_argument("--poll", type=int, default=10)
    ap.add_argument("--timeout", type=int, default=7200)
    args = ap.parse_args()

    base = req_env("AAP_BASE_URL").rstrip("/")
    token = req_env("AAP_TOKEN")
    jt = int(req_env("AAP_JOB_TEMPLATE_ID"))
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json", "Accept":"application/json"}

    extra_vars = json.loads(args.extra_vars)

    r = requests.post(f"{base}/api/v2/job_templates/{jt}/launch/", headers=headers,
                      json={"limit": args.limit, "extra_vars": extra_vars}, timeout=60)
    if r.status_code >= 400:
        print(f"Launch failed {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)
    job_id = int((r.json().get("job") or r.json().get("id")))
    print("Launched AAP job:", job_id)

    start = time.time()
    last = None
    while True:
        j = requests.get(f"{base}/api/v2/jobs/{job_id}/", headers=headers, timeout=60)
        if j.status_code >= 400:
            print(f"Status fetch failed {j.status_code}: {j.text}", file=sys.stderr)
            sys.exit(1)
        status = j.json().get("status")
        if status != last:
            print("Status:", status)
            last = status
        if status in TERMINAL:
            print("Final status:", status)
            sys.exit(0 if status == "successful" else 1)
        if time.time() - start > args.timeout:
            print(f"Timed out waiting for job {job_id}", file=sys.stderr)
            sys.exit(1)
        time.sleep(args.poll)

if __name__ == "__main__":
    main()
