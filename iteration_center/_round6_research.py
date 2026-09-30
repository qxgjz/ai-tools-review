"""Round 6: Find new keyword opportunities via Serper API"""
import requests, json, os, time

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
HEADERS = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}

# New seed keywords to explore - gaps in our current coverage
# Focus on: AI tools we haven't covered, comparison patterns, alternatives
SEEDS = [
    # New comparison keywords
    ("notion-ai-vs-obsidian-ai", "Notion AI vs Obsidian AI"),
    ("chatgpt-vs-gemini-2026", "ChatGPT vs Gemini 2026"),
    ("midjourney-v7-vs-flux", "Midjourney v7 vs Flux"),
    # New alternatives keywords
    ("jasper-alternatives", "Jasper alternatives"),
    ("grammarly-alternatives", "Grammarly alternatives"),
    ("surfer-seo-alternatives", "Surfer SEO alternatives"),
    ("canva-ai-alternatives", "Canva AI alternatives"),
    ("hubsopt-ai-alternatives", "HubSpot AI alternatives"),
    ("zapier-ai-alternatives", "Zapier AI alternatives"),
    ("elevenlabs-alternatives", "ElevenLabs alternatives"),
    # New review keywords
    ("plandex-ai-review", "Plandex AI review"),
    ("roo-code-review", "Roo Code review"),
    ("crawl4ai-review", "Crawl4AI review"),
]

results = {}

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
        
        top_urls = [{"title": o.get("title",""), "url": o.get("link",""), "domain": o.get("link","").split("/")[2] if "://" in o.get("link","") else ""} for o in organic[:3]]
        paa_q = [p.get("question","") for p in paa[:4]]
        
        # Quick KD estimate: count weak domains
        weak_domains = {"reddit.com", "medium.com", "substack.com", "quora.com", 
                       "youtube.com", "blogspot.com", "wordpress.com", "github.io"}
        weak_count = sum(1 for u in top_urls if any(wd in u["domain"] for wd in weak_domains))
        
        results[slug] = {
            "keyword": kw,
            "top_competitors": top_urls,
            "paa": paa_q,
            "weak_domains_in_top3": weak_count,
            "kd_estimate": "low" if weak_count >= 2 else "medium",
        }
        
        print(f"  Top3: {[u['domain'] for u in top_urls]}")
        print(f"  Weak domains: {weak_count}/3")
        print(f"  PAA: {len(paa_q)} questions")
        for q in paa_q[:3]:
            print(f"    Q: {q[:60]}")
        time.sleep(0.8)
    except Exception as e:
        print(f"  ERROR: {e}")
        results[slug] = {"keyword": kw, "error": str(e)}

with open("iteration_center/keyword_research_round6.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n=== Done: {len(results)} keywords ===")
# Print summary table
print("\n=== Summary ===")
for slug, r in results.items():
    if "error" in r:
        print(f"  {slug}: ERROR")
    else:
        print(f"  {slug}: KD={r['kd_estimate']}, weak={r['weak_domains_in_top3']}/3, PAA={len(r['paa'])}")
