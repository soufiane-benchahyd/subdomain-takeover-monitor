import json
import pandas as pd

results = []
with open("data/http_responses/fingerprint_results.jsonl") as f:
    for line in f:
        results.append(json.loads(line))

df = pd.DataFrame(results)
confirmed = df[df["takeover_confirmed"] == True]
confirmed.to_csv("reports/confirmed_takeovers.csv", index=False)

print(f"\n{'='*50}")
print(f"Total scanned:         {len(df)}")
print(f"Pattern matched:       {len(df[df['matched_pattern']])}")
print(f"Takeovers confirmed:   {len(confirmed)}")
print(f"{'='*50}\n")
print(confirmed[["domain", "provider", "cname_target"]].to_string())