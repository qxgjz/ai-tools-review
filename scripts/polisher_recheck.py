"""Re-score the 3 polisher-updated articles only."""
import json, os, sys, re, tempfile
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

tmp = tempfile.mkdtemp(prefix="polis_recheck_")
for slug in targets:
    p = next(x for x in posts if x["slug"] == slug)
    content = p["content"]
    text = re.sub(r"<[^>]+>", "", content)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    fp = Path(tmp) / f"{slug[:50]}.md"
    fp.write_text(f"# {p['title']}\n\n{text}", encoding="utf-8")
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
            print(f"    - {c.get('check')}: {c.get('detail','')[:120]}")
