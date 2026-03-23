import pandas as pd
import json
from datetime import datetime

def generate_html_report():
    scored   = pd.read_csv("reports/scored_takeovers.csv")
    dangling = pd.read_csv("data/dns_results/dangling_cnames.csv")
    
    try:
        manifest = json.load(open("reports/data_manifest.json"))
    except FileNotFoundError:
        manifest = {}

    severity_colors = {
        "CRITICAL": "#ff4444",
        "HIGH":     "#ff8800",
        "MEDIUM":   "#ffcc00",
        "LOW":      "#44bb44"
    }

    rows = ""
    for _, row in scored.iterrows():
        color = severity_colors.get(row["severity"], "#999")
        rows += f"""
        <tr>
            <td><code>{row['domain']}</code></td>
            <td>{row['provider']}</td>
            <td><code>{row['cname_target']}</code></td>
            <td style="color:{color}; font-weight:bold">{row['severity']}</td>
            <td>{row['risk_score']}/10</td>
            <td>{row['impact']}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Subdomain Takeover Report</title>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; background: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }}
  h1   {{ color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; }}
  .stats {{ display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }}
  .stat-box {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px;
               padding: 15px 25px; text-align: center; min-width: 120px; }}
  .stat-box .num {{ font-size: 2em; font-weight: bold; color: #58a6ff; }}
  .stat-box .label {{ font-size: 0.85em; color: #8b949e; }}
  table {{ width: 100%; border-collapse: collapse; background: #161b22;
           border-radius: 8px; overflow: hidden; margin-top: 20px; }}
  th    {{ background: #21262d; padding: 12px; text-align: left;
           color: #8b949e; font-size: 0.85em; text-transform: uppercase; }}
  td    {{ padding: 12px; border-top: 1px solid #30363d; font-size: 0.9em; }}
  tr:hover {{ background: #1c2128; }}
  code  {{ background: #21262d; padding: 2px 6px; border-radius: 4px;
           font-size: 0.85em; color: #79c0ff; }}
  .footer {{ margin-top: 30px; color: #8b949e; font-size: 0.8em; }}
  .badge-critical {{ color: #ff4444; font-weight: bold; }}
  .badge-high     {{ color: #ff8800; font-weight: bold; }}
  .badge-medium   {{ color: #ffcc00; font-weight: bold; }}
  .badge-low      {{ color: #44bb44; font-weight: bold; }}
</style>
</head>
<body>

<h1>🔍 Subdomain Takeover Monitor — Findings Report</h1>
<p style="color:#8b949e">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} &nbsp;|&nbsp; 
Tool: Subdomain Takeover Monitor &nbsp;|&nbsp; 
For authorized security research only</p>

<div class="stats">
  <div class="stat-box">
    <div class="num">{len(dangling)}</div>
    <div class="label">Dangling CNAMEs</div>
  </div>
  <div class="stat-box">
    <div class="num">{len(scored)}</div>
    <div class="label">Confirmed Takeovers</div>
  </div>
  <div class="stat-box">
    <div class="num" style="color:#ff4444">
      {len(scored[scored.severity == 'CRITICAL'])}
    </div>
    <div class="label">Critical</div>
  </div>
  <div class="stat-box">
    <div class="num" style="color:#ff8800">
      {len(scored[scored.severity == 'HIGH'])}
    </div>
    <div class="label">High</div>
  </div>
  <div class="stat-box">
    <div class="num" style="color:#ffcc00">
      {len(scored[scored.severity == 'MEDIUM'])}
    </div>
    <div class="label">Medium</div>
  </div>
  <div class="stat-box">
    <div class="num" style="color:#44bb44">
      {len(scored[scored.severity == 'LOW'])}
    </div>
    <div class="label">Low</div>
  </div>
</div>

<table>
  <thead>
    <tr>
      <th>Domain</th>
      <th>Provider</th>
      <th>CNAME Target</th>
      <th>Severity</th>
      <th>Score</th>
      <th>Impact</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>

<div class="footer">
  <p>Scanned {len(dangling)} dangling CNAMEs across monitored domains.</p>
  <p>⚠️ This report is for authorized security research and responsible disclosure only.</p>
</div>

</body>
</html>"""

    with open("reports/takeover_report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[+] Report saved to reports/takeover_report.html")

if __name__ == "__main__":
    generate_html_report()