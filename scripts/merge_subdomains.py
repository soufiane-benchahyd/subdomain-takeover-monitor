import pandas as pd
import glob
import json

files = glob.glob("data/ct_logs/*.csv")
all_domains = set()

# Read CSV files
for f in files:
    df = pd.read_csv(f)
    all_domains.update(df["subdomain"].dropna().tolist())

# Read JSONL (certstream) if exists
try:
    with open("data/ct_logs/ct_stream.jsonl") as f:
        for line in f:
            entry = json.loads(line)
            for d in entry["domains"]:
                all_domains.add(d.lstrip("*."))
except FileNotFoundError:
    print("[!] No certstream file found, skipping...")

master = pd.DataFrame({"subdomain": list(all_domains)})
master.to_csv("data/dns_results/master_subdomains.csv", index=False)

print(f"[+] Total unique subdomains: {len(master)}")