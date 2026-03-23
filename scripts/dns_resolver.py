import asyncio
import dns.asyncresolver
import pandas as pd
import json
from tqdm.asyncio import tqdm

INPUT = "data/dns_results/master_subdomains.csv"
OUTPUT = "data/dns_results/dns_resolved.jsonl"

async def resolve(domain, semaphore):
    result = {
        "domain": domain,
        "a": [],
        "cname": [],
        "ns": [],
        "mx": [],
        "error": None
    }

    async with semaphore:
        resolver = dns.asyncresolver.Resolver()
        resolver.timeout = 3
        resolver.lifetime = 3

        for rtype in ["A", "CNAME", "NS", "MX"]:
            try:
                answers = await resolver.resolve(domain, rtype)
                result[rtype.lower()] = [r.to_text() for r in answers]
            except Exception:
                result[rtype.lower()] = []

    return result


async def main():
    df = pd.read_csv(INPUT)
    domains = df["subdomain"].dropna().tolist()

    semaphore = asyncio.Semaphore(100)  # safer than 200 on Windows

    with open(OUTPUT, "w") as out:
        tasks = [resolve(d, semaphore) for d in domains]

        for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            result = await coro
            out.write(json.dumps(result) + "\n")

    print(f"\n[+] Done. Results saved to {OUTPUT}")


asyncio.run(main())