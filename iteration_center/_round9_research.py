"""Round 9: Mine new keyword gaps via Serper API"""
import requests, json, os, time

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
HEADERS = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}

SEEDS = [
    # Comparison gaps
    ("chatgpt-vs-grok", "ChatGPT vs Grok"),
    ("claude-vs-copilot", "Claude vs Microsoft Copilot"),
    ("gemini-vs-grok", "Gemini vs Grok"),
    # Alternatives gaps
    ("midjourney-v7-alternatives", "Midjourney v7 alternatives"),
    ("elevenlabs-alternatives", "ElevenLabs alternatives"),
    ("synthesia-alternatives", "Synthesia alternatives"),
    ("heygen-vs-synthesia", "HeyGen vs Synthesia"),
    # Review gaps
    ("deepseek-review", "DeepSeek review"),
    ("kimi-review", "Kimi AI review"),
    ("qwen-review", "Qwen AI review"),
    ("grok-3-review", "Grok 3 review"),
    ("notebooklm-review", "NotebookLM review"),
    # How-to / tutorial gaps
    ("how-to-use-chatgpt-for-coding", "how to use ChatGPT for coding"),
    ("how-to-use-claude-for-writing", "how to use Claude for writing"),
]

results = {}
weak_domains = {"reddit.com", "medium.com", "substack.com", "quora.com",
                "youtube.com", "blogspot.com", "wordpress.com", "github.io",
                "github.com", "news.ycombinator.com", "trustpilot.com"}

# Skip already covered
SKIP = {
    "elevenlabs-alternatives",  # round6 brief exists
    "synthesia-vs-heygen",  # existing
    "deepseek-review",  # check later
}

for slug, kw in SEEDS:
    if slug in SKIP:
        print(f"SKIP {slug}")
        continue
    print(f"\n=== {kw} ===")
    try:
        r = requests.post(
            "https://google.serper.dev/search",
            headers=HEADERS,
            json={"q": kw, "num": 10},
            timeout=30
        )
        data = r.json()
        organic = data.get("organic", [])[:5]
        paa = data.get("peopleAlsoAsk", [])[:6]
        top_urls = [{"title": o.get("title",""), "url": o.get("link",""),
                     "domain": o.get("link","").split("/")[2] if "://" in o.get("link","") else ""}
                    for o in organic[:3]]
        paa_q = [p.get("question","") for p in paa[:4]]
        weak_count = sum(1 for u in top_urls if any(wd in u["domain"] for wd in weak_domains))
        results[slug] = {
            "keyword": kw, "top_competitors": top_urls, "paa": paa_q,
            "weak_domains_in_top3": weak_count,
            "kd_estimate": "low" if weak_count >= 2 else "medium",
        }
        print(f"  Top3: {[u['domain'] for u in top_urls]}, Weak: {weak_count}/3, PAA: {len(paa_q)}")
        time.sleep(0.8)
    except Exception as e:
        print(f"  ERROR: {e}")
        results[slug] = {"keyword": kw, "error": str(e)}

with open("iteration_center/keyword_research_round9.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n=== Done: {len(results)} keywords ===")
low = [(s,r) for s,r in results.items() if "error" not in r and r["kd_estimate"]=="low"]
med = [(s,r) for s,r in results.items() if "error" not in r and r["kd_estimate"]=="medium"]
print(f"\nLOW KD ({len(low)}):")
for s,r in low:
    print(f"  {s}: weak={r['weak_domains_in_top3']}/3, PAA={len(r['paa'])}")
print(f"MEDIUM KD ({len(med)}):")
for s,r in med:
    print(f"  {s}: weak={r['weak_domains_in_top3']}/3, PAA={len(r['paa'])}")
