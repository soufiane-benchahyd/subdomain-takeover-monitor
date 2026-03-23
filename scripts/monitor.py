# scripts/monitor.py
import time
import subprocess
import schedule
import json
from datetime import datetime

LOG = "reports/monitor_log.jsonl"

def run_pipeline():
    print(f"\n[{datetime.utcnow()}] Starting monitoring cycle...")
    steps = [
        ("Scraping crt.sh",      ["python", "scripts/crtsh_scraper.py", "microsoft.com"]),
        ("Merging subdomains",    ["python", "scripts/merge_subdomains.py"]),
        ("DNS resolution",        ["python", "scripts/dns_resolver.py"]),
        ("Flagging dangling",     ["python", "scripts/flag_dangling.py"]),
        ("HTTP fingerprinting",   ["python", "scripts/http_fingerprint.py"]),
        ("Scoring risks",         ["python", "scripts/risk_scorer.py"]),
        ("Generating report",     ["python", "scripts/generate_report.py"]),
    ]
    results = {}
    for name, cmd in steps:
        print(f"  [*] {name}...")
        r = subprocess.run(cmd, capture_output=True, text=True)
        results[name] = "OK" if r.returncode == 0 else f"ERROR: {r.stderr[:100]}"
        print(f"      {'✅' if r.returncode == 0 else '❌'} {results[name]}")

    entry = {"timestamp": str(datetime.utcnow()), "results": results}
    with open(LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"[+] Cycle complete. Log updated.")

# Run once immediately, then every 6 hours
run_pipeline()
schedule.every(6).hours.do(run_pipeline)

while True:
    schedule.run_pending()
    time.sleep(60)