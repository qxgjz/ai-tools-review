"""Batch research: 11 keywords -> SERP analysis -> briefs"""
import requests, json, os, time

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
HEADERS = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}

KEYWORDS = [
    ("lovable-vs-boltnew", "Lovable vs Bolt.new", "comparison", "AI app builders"),
    ("claude-37-vs-gpt4o", "Claude 3.7 vs GPT-4o", "comparison", "LLM comparison"),
    ("synthesia-vs-heygen", "Synthesia vs HeyGen", "comparison", "AI video generation"),
    ("runway-alternatives", "Runway ML alternatives", "alternatives", "AI video editing"),
    ("gemini-vs-perplexity", "Gemini vs Perplexity", "comparison", "AI search"),
    ("beautiful-ai-alternatives", "Beautiful.ai alternatives", "alternatives", "AI presentation"),
    ("devin-ai-review", "Devin AI review", "review", "AI software engineer"),
    ("writesonic-alternatives", "Writesonic alternatives", "alternatives", "AI writing"),
    ("motion-ai-alternatives", "Motion AI alternatives", "alternatives", "AI calendar scheduling"),
    ("clearscope-alternatives", "Clearscope alternatives", "alternatives", "SEO content optimization"),
    ("quillbot-alternatives", "QuillBot alternatives", "alternatives", "AI paraphrasing"),
]

results = {}

for slug, kw, ktype, category in KEYWORDS:
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
        paa = data.get("peopleAlsoAsk", [])[:8]
        
        print(f"  Top results: {len(organic)}")
        top_urls = []
        for o in organic[:3]:
            print(f"    - {o.get('title','')[:60]} | {o.get('link','')}")
            top_urls.append({"title": o.get("title",""), "url": o.get("link","")})
        
        print(f"  PAA: {len(paa)}")
        paa_questions = []
        for p in paa[:6]:
            print(f"    Q: {p.get('question','')[:70]}")
            paa_questions.append(p.get("question",""))
        
        results[slug] = {
            "keyword": kw,
            "type": ktype,
            "category": category,
            "top_competitors": top_urls,
            "paa": paa_questions,
        }
        time.sleep(1)
    except Exception as e:
        print(f"  ERROR: {e}")
        results[slug] = {"keyword": kw, "type": ktype, "category": category, "top_competitors": [], "paa": [], "error": str(e)}

# Save raw data
with open("iteration_center/keyword_research_round5.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n\n=== Done: {len(results)} keywords researched ===")
