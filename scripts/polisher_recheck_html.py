"""Re-score 3 articles as .html (so zens-ink uses HTML parser branch)."""
import json, os, sys, tempfile
from pathlib import Path

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")
sys.path.insert(0, "scripts")
from zens_ink import content_qc

posts = json.load(open("data/posts.json", "r", encoding="utf-8"))
targets = [
    "midjourney-v7-vs-flux-2026",
    "chatgpt-vs-claude-2026-comparison",
    "claude-37-vs-gpt4o",
]

tmp = tempfile.mkdtemp(prefix="polis_html_")
for slug in targets:
    p = next(x for x in posts if x["slug"] == slug)
    content = p["content"]
    # Wrap in minimal HTML doc so zens-ink HTML parser sees title/meta/h2/links
    html = f"""<!DOCTYPE html>
<html><head>
<title>{p['title']}</title>
<meta name="description" content="{p.get('excerpt','')[:160]}" />
<meta name="date" content="{p.get('publishedAt','')[:10]}" />
</head><body>
<h1>{p['title']}</h1>
{content}
</body></html>"""
    fp = Path(tmp) / f"{slug[:50]}.html"
    fp.write_text(html, encoding="utf-8")
    res = content_qc.check_draft(fp)
    print("=" * 70)
    print(f"SLUG: {slug}")
    print(f"  score: {res.get('score')}")
    print(f"  word_count: {res.get('word_count')}")
    print(f"  fact_density: {res.get('fact_density')}")
    print(f"  vague_density: {res.get('vague_density')}")
    print(f"  FAILED checks:")
    for c in res.get("checks", []):
        if not c.get("pass"):
            print(f"    - {c.get('check')} (w={c.get('weight')}): {c.get('note','')[:100]}")
