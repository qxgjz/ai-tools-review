"""Round 10: Mine new keyword gaps"""
import requests, json, os, time

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")
SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
HEADERS = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}

SEEDS = [
    # Comparison gaps
    ("gpt-5-vs-claude-opus", "GPT-5 vs Claude Opus"),
    ("gemini-25-vs-gpt5", "Gemini 2.5 vs GPT-5"),
    ("cursor-vs-windsurf-2026", "Cursor vs Windsurf 2026"),
    # Alternatives gaps
    ("jasper-ai-alternatives", "Jasper AI alternatives"),
    ("writesonic-alternatives", "Writesonic alternatives"),
    ("surfer-seo-alternatives", "Surfer SEO alternatives"),
    ("clearscope-alternatives", "Clearscope alternatives"),
    ("beautiful-ai-alternatives", "Beautiful.ai alternatives"),
    # Review gaps
    ("v0-dev-review", "v0.dev review"),
    ("replit-ai-review", "Replit AI review"),
    ("lovable-review", "Lovable review"),
    ("devin-ai-review", "Devin AI review"),
    ("manus-ai-review", "Manus AI review"),
    ("openai-o3-review", "OpenAI o3 review"),
]

SKIP = {
    "writesonic-alternatives", "surfer-seo-alternatives", "clearscope-alternatives",
    "beautiful-ai-alternatives", "devin-ai-review", "replit-ai-review",
    "v0-dev-review",  # partially covered
}

results = {}
weak = {"reddit.com","medium.com","substack.com","quora.com","youtube.com",
        "blogspot.com","wordpress.com","github.io","github.com","trustpilot.com"}

for slug, kw in SEEDS:
    if slug in SKIP:
        continue
    print(f"=== {kw} ===")
    try:
        r = requests.post("https://google.serper.dev/search", headers=HEADERS,
                         json={"q": kw, "num": 10}, timeout=30)
        data = r.json()
        organic = data.get("organic", [])[:3]
        paa = data.get("peopleAlsoAsk", [])[:6]
        tops = [{"title": o.get("title",""), "url": o.get("link",""),
                 "domain": o.get("link","").split("/")[2] if "://" in o.get("link","") else ""}
                for o in organic]
        paa_q = [p.get("question","") for p in paa[:4]]
        wc = sum(1 for u in tops if any(d in u["domain"] for d in weak))
        results[slug] = {"keyword": kw, "top_competitors": tops, "paa": paa_q,
                         "weak_in_top3": wc,
                         "kd": "low" if wc >= 2 else "medium"}
        print(f"  Top3: {[u['domain'] for u in tops]}, weak={wc}/3, PAA={len(paa_q)}")
        time.sleep(0.8)
    except Exception as e:
        print(f"  ERR: {e}")

with open("iteration_center/keyword_research_round10.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

low = [(s,r) for s,r in results.items() if r["kd"]=="low"]
med = [(s,r) for s,r in results.items() if r["kd"]=="medium"]
print(f"\nLOW ({len(low)}): {[s for s,_ in low]}")
print(f"MED ({len(med)}): {[s for s,_ in med]}")
