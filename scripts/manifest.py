import os, json, glob

manifest = {}
for folder in ["data/ct_logs", "data/dns_results", "data/http_responses", "reports"]:
    files = glob.glob(f"{folder}/*")
    manifest[folder] = {
        "files": [os.path.basename(f) for f in files],
        "total_size_mb": round(sum(os.path.getsize(f) for f in files) / 1e6, 2)
    }

with open("reports/data_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(json.dumps(manifest, indent=2))