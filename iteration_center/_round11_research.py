"""Round 11: Mine new keyword gaps"""
import requests, json, os, time

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")
SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
HEADERS = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}

SEEDS = [
    # More comparison gaps
    ("grok-vs-gemini", "Grok vs Gemini"),
    ("claude-opus-vs-gpt5", "Claude Opus vs GPT-5"),
    ("deepseek-vs-gpt", "DeepSeek vs GPT"),
    # More alternatives
    ("otter-ai-alternatives", "Otter.ai alternatives"),
    ("fireflies-ai-alternatives", "Fireflies.ai alternatives"),
    # Review gaps
    ("qwen-ai-review", "Qwen AI review"),
    ("deepseek-review", "DeepSeek R1 review"),
    ("perplexity-enterprise-review", "Perplexity Enterprise review"),
    # How-to
    ("best-ai-voice-generator", "best AI voice generator"),
    ("best-ai-headshot-generator", "best AI headshot generator"),
    ("best-ai-slack-bots", "best AI Slack bots"),
]

SKIP = {
    "otter-ai-alternatives",  # existing brief
    "fireflies-ai-alternatives",  # round8 brief
    "deepseek-review",  # already checked
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
        print(f"  Top3: {[u['domain'] for u in tops]}, weak={wc}/3")
        time.sleep(0.8)
    except Exception as e:
        print(f"  ERR: {e}")

with open("iteration_center/keyword_research_round11.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

low = [(s,r) for s,r in results.items() if r["kd"]=="low"]
med = [(s,r) for s,r in results.items() if r["kd"]=="medium"]
print(f"\nLOW ({len(low)}): {[s for s,_ in low]}")
print(f"MED ({len(med)}): {[s for s,_ in med]}")
