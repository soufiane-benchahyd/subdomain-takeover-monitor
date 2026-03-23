import asyncio
import aiohttp
import json
import pandas as pd
from tqdm.asyncio import tqdm

INPUT = "data/dns_results/dangling_cnames.csv"
OUTPUT = "data/http_responses/fingerprint_results.jsonl"
FINGERPRINTS = json.load(open("configs/fingerprints.json"))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SecurityResearch/1.0)"
}

async def fingerprint(session, row, semaphore):
    domain = row["domain"]
    provider = row["provider"]
    result = {
        "domain": domain,
        "provider": provider,
        "cname_target": row["cname_target"],
        "status_code": None,
        "matched_pattern": False,
        "takeover_confirmed": False,
        "response_snippet": "",
        "error": None
    }
    async with semaphore:
        for scheme in ["https", "http"]:
            try:
                url = f"{scheme}://{domain}"
                async with session.get(url, headers=HEADERS,
                                       timeout=aiohttp.ClientTimeout(total=8),
                                       allow_redirects=True,
                                       ssl=False) as resp:
                    result["status_code"] = resp.status
                    body = await resp.text(errors="ignore")
                    result["response_snippet"] = body[:500]
                    fp = FINGERPRINTS.get(provider, {})
                    pattern = fp.get("pattern", "")
                    if pattern and pattern.lower() in body.lower():
                        result["matched_pattern"] = True
                        result["takeover_confirmed"] = fp.get("takeover", False)
                    break
            except Exception as e:
                result["error"] = str(e)
    return result

async def main():
    df = pd.read_csv(INPUT)
    semaphore = asyncio.Semaphore(100)
    connector = aiohttp.TCPConnector(limit=100, ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fingerprint(session, row, semaphore) for _, row in df.iterrows()]
        with open(OUTPUT, "w") as out:
            for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
                result = await coro
                out.write(json.dumps(result) + "\n")
                if result["takeover_confirmed"]:
                    print(f"[!!!] CONFIRMED TAKEOVER: {result['domain']} -> {result['provider']}")

asyncio.run(main())