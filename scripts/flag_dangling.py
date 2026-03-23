import json
import pandas as pd

KNOWN_DEAD_PATTERNS = [
    "s3.amazonaws.com",
    "github.io",
    "herokuapp.com",
    "azurewebsites.net",
    "cloudapp.net",
    "trafficmanager.net",
    "ghost.io",
    "fastly.net",
    "helpscoutdocs.com",
    "uservoice.com",
    "zendesk.com",
    "freshdesk.com",
    "surge.sh",
    "bitbucket.io",
    "smugmug.com",
    "webflow.io",
    "pantheonsite.io",
    "tumblr.com",
    "squarespace.com",
    "wpengine.com"
]

dangling = []

with open("data/dns_results/dns_resolved.jsonl") as f:
    for line in f:
        record = json.loads(line)
        cnames = record.get("cname", [])
        a_records = record.get("a", [])
        for cname in cnames:
            for pattern in KNOWN_DEAD_PATTERNS:
                if pattern in cname:
                    dangling.append({
                        "domain": record["domain"],
                        "cname_target": cname,
                        "provider": pattern,
                        "has_a_record": len(a_records) > 0
                    })

df = pd.DataFrame(dangling)
df.to_csv("data/dns_results/dangling_cnames.csv", index=False)

print(f"[!] Found {len(df)} potential dangling CNAMEs")
print(df.head(20).to_string())