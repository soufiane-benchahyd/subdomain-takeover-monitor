
```markdown
# 🔍 Subdomain Takeover Monitor

A automated security research pipeline that detects subdomain takeover vulnerabilities by monitoring Certificate Transparency logs, performing bulk DNS resolution, and fingerprinting dangling CNAME records across cloud providers.

Built as a portfolio project demonstrating real-world offensive reconnaissance and responsible disclosure practices.

---

## 🎯 Real Findings

This tool detected **8 confirmed subdomain takeover vulnerabilities** in a single run:

| Severity | Count | Targets |
|----------|-------|---------|
| 🔴 CRITICAL | 2 | github.com |
| 🟠 HIGH | 6 | microsoft.com |

> ⚠️ All findings were responsibly disclosed to Microsoft MSRC and GitHub Security. No exploitation was performed.

---

## 📊 Sample Report

![Findings Report](reports/takeover_report_screenshot.png)

---

## 🏗 Architecture

```
CT Logs (certstream + crt.sh)
        ↓
Subdomain Harvesting (4,000–6,000 subdomains)
        ↓
Bulk Async DNS Resolution (200 concurrent)
        ↓
Dangling CNAME Detection (25+ cloud providers)
        ↓
HTTP Fingerprinting (pattern matching per provider)
        ↓
Risk Scoring (CRITICAL / HIGH / MEDIUM / LOW)
        ↓
HTML Report + Continuous Monitoring Loop
```

---

## ⚙️ Pipeline Steps

| Script | Purpose |
|--------|---------|
| `scripts/crtsh_scraper.py` | Harvest subdomains from crt.sh certificate transparency logs |
| `scripts/ct_stream.py` | Stream live CT log events via certstream |
| `scripts/merge_subdomains.py` | Deduplicate and merge all collected subdomains |
| `scripts/dns_resolver.py` | Async DNS resolution (A, CNAME, NS, MX records) |
| `scripts/flag_dangling.py` | Detect dangling CNAMEs pointing to unclaimed cloud resources |
| `scripts/http_fingerprint.py` | HTTP/HTTPS fingerprinting against provider error patterns |
| `scripts/risk_scorer.py` | Score findings by severity and potential impact |
| `scripts/generate_report.py` | Generate HTML findings report |
| `scripts/monitor.py` | Continuous monitoring loop (runs every 6 hours) |
| `main.py` | Single CLI entry point for full pipeline |

---

## 🚀 Quick Start

```bash
git clone https://github.com/soufiane-benchahyd/subdomain-takeover-monitor.git
cd subdomain-takeover-monitor
python -m venv venv
.\venv\Scripts\Activate.ps1       # Windows
# source venv/bin/activate        # Linux/Mac
pip install -r requirements.txt
python main.py
```

### Run individual steps
```bash
python main.py scrape       # CT log harvesting only
python main.py resolve      # DNS resolution only
python main.py fingerprint  # HTTP fingerprinting only
python main.py report       # Generate HTML report only
python main.py monitor      # Start continuous monitoring loop
```

---

## 🔬 How It Works

### 1. Subdomain Harvesting
Queries crt.sh Certificate Transparency logs for subdomains of target domains. CT logs record every TLS certificate issued, making them a rich passive recon source with no direct target interaction.

### 2. Async DNS Resolution
Resolves A, CNAME, NS, and MX records for all collected subdomains using async DNS with 200 concurrent resolvers. Identifies subdomains with CNAME chains pointing to cloud providers.

### 3. Dangling CNAME Detection
Cross-references CNAME targets against a database of 25+ cloud provider patterns. A dangling CNAME exists when a subdomain points to a cloud resource that no longer exists.

### 4. HTTP Fingerprinting
Sends HTTP/HTTPS requests to each dangling subdomain and matches response bodies against provider-specific error signatures to confirm takeover viability.

### 5. Risk Scoring
Scores each confirmed finding based on provider, potential for XSS, phishing, cookie scope abuse, and ease of exploitation.

---

## 🏭 Supported Providers (25+)

GitHub Pages, AWS S3, Azure Web Apps, Heroku, Surge.sh, Ghost.io,
Webflow, Fastly, Pantheon, HelpScout, UserVoice, Zendesk, Freshdesk,
Bitbucket, Tumblr, WPEngine, Readme.io, Aftership, Pingdom, and more.

---

## ⚠️ Legal & Ethical Use

This tool is intended for:
- Authorized security research
- Bug bounty programs
- Security teams monitoring their own infrastructure

**Do not run this tool against domains you do not own or have explicit permission to test.**
All findings produced during development were responsibly disclosed to affected vendors.

---

## 🛠 Tech Stack

- **Python 3.x** — core pipeline
- **dnspython** — async DNS resolution
- **aiohttp** — async HTTP fingerprinting
- **certstream** — live CT log streaming
- **pandas** — data processing and deduplication
- **rich / tqdm** — CLI output and progress bars
- **schedule** — monitoring loop

---

## 📁 Project Structure

```
subdomain-takeover-monitor/
├── configs/
│   └── fingerprints.json        # Provider fingerprint database
├── data/
│   ├── ct_logs/                 # Raw CT log and crt.sh data
│   ├── dns_results/             # DNS resolution output
│   └── http_responses/          # HTTP fingerprint results
├── reports/
│   ├── confirmed_takeovers.csv  # Raw confirmed findings
│   ├── scored_takeovers.csv     # Risk-scored findings
│   ├── takeover_report.html     # Final HTML report
│   └── takeover_report_screenshot.png  # Report screenshot
├── scripts/                     # Pipeline modules
├── main.py                      # CLI entry point
└── requirements.txt
```

---

## 📬 Responsible Disclosure

Findings from this tool have been reported to:
- **Microsoft MSRC** — msrc.microsoft.com/report
- **GitHub Security** — via HackerOne

*Disclosure confirmations pending.*
```
