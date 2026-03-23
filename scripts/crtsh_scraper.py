import requests
import pandas as pd
import sys

def query_crtsh(domain):
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    r = requests.get(url, timeout=120)
    if r.status_code != 200:
        return []
    data = r.json()
    domains = set()
    for entry in data:
        name = entry.get("name_value", "")
        for line in name.splitlines():
            line = line.strip().lstrip("*.")
            if line:
                domains.add(line)
    return list(domains)

if __name__ == "__main__":
    target = sys.argv[1]
    results = query_crtsh(target)
    df = pd.DataFrame({"subdomain": results})
    out = f"data/ct_logs/crtsh_{target}.csv"
    df.to_csv(out, index=False)
    print(f"[+] Saved {len(results)} subdomains to {out}")