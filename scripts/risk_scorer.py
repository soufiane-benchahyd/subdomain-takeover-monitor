# scripts/risk_scorer.py
import json
import pandas as pd

PROVIDER_RISK = {
    "github.io":          {"score": 9, "severity": "CRITICAL", "reason": "Full HTML/JS control, XSS on parent domain possible"},
    "s3.amazonaws.com":   {"score": 9, "severity": "CRITICAL", "reason": "Serve arbitrary content, phishing, credential harvesting"},
    "herokuapp.com":      {"score": 8, "severity": "HIGH",     "reason": "Full app deployment possible"},
    "azurewebsites.net":  {"score": 8, "severity": "HIGH",     "reason": "Full app deployment, cookie scope abuse"},
    "ghost.io":           {"score": 7, "severity": "HIGH",     "reason": "Content injection, phishing"},
    "surge.sh":           {"score": 7, "severity": "HIGH",     "reason": "Static file hosting, phishing pages"},
    "webflow.io":         {"score": 6, "severity": "MEDIUM",   "reason": "Visual site cloning possible"},
    "fastly.net":         {"score": 6, "severity": "MEDIUM",   "reason": "CDN endpoint hijack"},
    "pantheonsite.io":    {"score": 5, "severity": "MEDIUM",   "reason": "WordPress hosting takeover"},
    "helpscoutdocs.com":  {"score": 4, "severity": "LOW",      "reason": "Documentation subdomain hijack"},
    "uservoice.com":      {"score": 4, "severity": "LOW",      "reason": "Feedback portal hijack"},
    "zendesk.com":        {"score": 4, "severity": "LOW",      "reason": "Support portal hijack"},
}

def score_results():
    df = pd.read_csv("reports/confirmed_takeovers.csv")
    
    scores = []
    for _, row in df.iterrows():
        provider = row.get("provider", "")
        risk = PROVIDER_RISK.get(provider, {
            "score": 3, "severity": "LOW", "reason": "Unknown provider"
        })
        scores.append({
            "domain":        row["domain"],
            "cname_target":  row["cname_target"],
            "provider":      provider,
            "risk_score":    risk["score"],
            "severity":      risk["severity"],
            "impact":        risk["reason"]
        })
    
    scored = pd.DataFrame(scores).sort_values("risk_score", ascending=False)
    scored.to_csv("reports/scored_takeovers.csv", index=False)
    
    print("\n=== RISK SUMMARY ===")
    print(scored[["domain", "provider", "severity", "risk_score"]].to_string(index=False))
    print(f"\nCRITICAL : {len(scored[scored.severity == 'CRITICAL'])}")
    print(f"HIGH     : {len(scored[scored.severity == 'HIGH'])}")
    print(f"MEDIUM   : {len(scored[scored.severity == 'MEDIUM'])}")
    print(f"LOW      : {len(scored[scored.severity == 'LOW'])}")
    return scored

if __name__ == "__main__":
    score_results()