"""Round 8: Mine new keyword gaps via Serper API"""
import requests, json, os, time

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
HEADERS = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}

# Round 8: fresh gaps not covered by 137 posts + 29 briefs
SEEDS = [
    # Comparison gaps
    ("perplexity-vs-grok", "Perplexity vs Grok"),
    ("claude-37-vs-opus", "Claude 3.7 vs Opus"),
    ("copilot-vs-gemini", "Microsoft Copilot vs Gemini"),
    # Alternatives gaps
    ("jasper-ai-alternatives", "Jasper AI alternatives"),
    ("copy-ai-alternatives", "Copy.ai alternatives"),
    ("motion-ai-alternatives", "Motion AI alternatives"),
    ("otter-ai-alternatives", "Otter.ai alternatives"),
    ("fireflies-ai-alternatives", "Fireflies.ai alternatives"),
    # Review gaps
    ("boltnew-review", "Bolt.new review"),
    ("replit-ai-review", "Replit AI review"),
    ("devin-ai-review", "Devin AI review"),
    ("v0-dev-review", "v0.dev review"),
    ("aider-review", "Aider review"),
    ("plandex-review", "Plandex review"),
    ("codeium-review", "Codeium review"),
    ("tabnine-review", "Tabnine review"),
]

results = {}
weak_domains = {"reddit.com", "medium.com", "substack.com", "quora.com",
                "youtube.com", "blogspot.com", "wordpress.com", "github.io",
                "github.com", "news.ycombinator.com", "trustpilot.com"}

for slug, kw in SEEDS:
    # Skip if already have a post or brief
    existing_slugs = [
        "jasper-ai-alternative-2026", "copy-ai-review-2026", "motion-ai-alternatives",
        "otter-ai-alternatives", "devin-ai-review", "replit-review-2026",
        "tabnine-review-2026", "writesonic-alternatives", "clearscope-alternatives",
        "beautiful-ai-alternatives", "suno-alternatives", "runway-alternatives",
        "sudowrite-alternatives", "quillbot-alternatives", "gemini-vs-perplexity",
        "claude-37-vs-gpt4o",
    ]
    if slug in [s.replace("-","_") for s in existing_slugs] or slug in existing_slugs:
        print(f"SKIP {slug} (already covered)")
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

with open("iteration_center/keyword_research_round8.json", "w", encoding="utf-8") as f:
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
