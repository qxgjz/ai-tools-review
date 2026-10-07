"""Round 7: Mine new keyword gaps via Serper API"""
import requests, json, os, time

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
HEADERS = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}

# New keywords to explore - gaps not covered by existing 137 posts
SEEDS = [
    # New comparison keywords
    ("perplexity-vs-gemini", "Perplexity vs Gemini"),
    ("claude-vs-perplexity", "Claude vs Perplexity"),
    ("cursor-vs-aider", "Cursor vs Aider"),
    ("v0-vs-lovable", "v0 vs Lovable"),
    # New alternatives keywords
    ("notion-ai-alternatives", "Notion AI alternatives"),
    ("midjourney-alternatives", "Midjourney alternatives"),
    ("pika-alternatives", "Pika alternatives"),
    ("heygen-alternatives", "HeyGen alternatives"),
    ("suno-alternatives", "Suno alternatives"),
    ("dify-alternatives", "Dify alternatives"),
    ("zapier-ai-alternatives", "Zapier AI alternatives"),
    ("hubsopt-ai-alternatives", "HubSpot AI alternatives"),
    # New review keywords
    ("boltnew-review", "Bolt.new review"),
    ("v0-dev-review", "v0.dev review"),
    ("aider-review", "Aider AI review"),
    ("n8n-ai-review", "n8n AI review"),
]

results = {}
weak_domains = {"reddit.com", "medium.com", "substack.com", "quora.com",
                "youtube.com", "blogspot.com", "wordpress.com", "github.io",
                "github.com", "news.ycombinator.com"}

for slug, kw in SEEDS:
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
            "keyword": kw,
            "top_competitors": top_urls,
            "paa": paa_q,
            "weak_domains_in_top3": weak_count,
            "kd_estimate": "low" if weak_count >= 2 else "medium",
        }
        
        print(f"  Top3: {[u['domain'] for u in top_urls]}")
        print(f"  Weak: {weak_count}/3, PAA: {len(paa_q)}")
        time.sleep(0.8)
    except Exception as e:
        print(f"  ERROR: {e}")
        results[slug] = {"keyword": kw, "error": str(e)}

with open("iteration_center/keyword_research_round7.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n=== Done: {len(results)} keywords ===")
print("\n=== Summary (low KD first) ===")
low = [(s,r) for s,r in results.items() if "error" not in r and r["kd_estimate"]=="low"]
med = [(s,r) for s,r in results.items() if "error" not in r and r["kd_estimate"]=="medium"]
print(f"LOW KD ({len(low)}):")
for s,r in low:
    print(f"  {s}: weak={r['weak_domains_in_top3']}/3, PAA={len(r['paa'])}")
print(f"MEDIUM KD ({len(med)}):")
for s,r in med:
    print(f"  {s}: weak={r['weak_domains_in_top3']}/3, PAA={len(r['paa'])}")
