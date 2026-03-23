# main.py
import argparse
import subprocess
import sys

STEPS = {
    "scrape":       ("Scrape CT logs + crt.sh",    "scripts/crtsh_scraper.py"),
    "merge":        ("Merge subdomains",            "scripts/merge_subdomains.py"),
    "resolve":      ("DNS resolution",              "scripts/dns_resolver.py"),
    "flag":         ("Flag dangling CNAMEs",        "scripts/flag_dangling.py"),
    "fingerprint":  ("HTTP fingerprinting",         "scripts/http_fingerprint.py"),
    "score":        ("Risk scoring",                "scripts/risk_scorer.py"),
    "report":       ("Generate HTML report",        "scripts/generate_report.py"),
    "monitor":      ("Start monitoring loop",       "scripts/monitor.py"),
}

def run_all():
    targets = ["microsoft.com", "github.com", "shopify.com", "amazonaws.com"]
    
    for key, (name, script) in STEPS.items():
        if key == "monitor":
            continue
        print(f"[*] {name}...")
        
        # crtsh_scraper needs domain arguments
        if "crtsh_scraper" in script:
            for target in targets:
                print(f"    Scraping {target}...")
                r = subprocess.run([sys.executable, script, target], capture_output=False)
        else:
            r = subprocess.run([sys.executable, script], capture_output=False)
            if r.returncode != 0:
                print(f"[!] Failed at: {name}")
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain Takeover Monitor")
    parser.add_argument("command", nargs="?", default="all",
                        choices=list(STEPS.keys()) + ["all"],
                        help="Step to run (default: all)")
    args = parser.parse_args()

    if args.command == "all":
        run_all()
    else:
        name, script = STEPS[args.command]
        print(f"[*] Running: {name}")
        subprocess.run([sys.executable, script])