"""Sample 10 articles and check layout + FAQ quality. Read-only audit."""
import json
import re
from pathlib import Path

POSTS = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\data\posts.json")

with open(POSTS, "r", encoding="utf-8") as f:
    posts = json.load(f)

print(f"Total posts: {len(posts)}")
print(f"Keys in first post: {list(posts[0].keys())}")

# Sample 10 evenly
n = len(posts)
idxs = [int(i * n / 10) for i in range(10)]
sample = [posts[i] for i in idxs]

results = []
for i, p in enumerate(sample):
    slug = p.get("slug", "?")
    title = p.get("title", "?")
    content = p.get("content", "") or p.get("body", "") or ""
    faqs = p.get("faqs", []) or p.get("faq", []) or []
    word_count = len(re.findall(r"\b\w+\b", content))
    img_count = len(re.findall(r"!\[", content))
    h1_count = len(re.findall(r"^# ", content, re.MULTILINE))
    h2_count = len(re.findall(r"^## ", content, re.MULTILINE))
    h3_count = len(re.findall(r"^### ", content, re.MULTILINE))
    has_intro = bool(re.search(r"(?i)(introduction|overview|what is|quick answer)", content[:2000]))
    has_conclusion = bool(re.search(r"(?i)(conclusion|final thoughts|summary|verdict)", content[-2000:]))
    results.append({
        "i": i, "slug": slug, "title": title[:60],
        "words": word_count, "imgs": img_count,
        "h1": h1_count, "h2": h2_count, "h3": h3_count,
        "has_intro": has_intro, "has_conclusion": has_conclusion,
        "faq_count": len(faqs),
        "faq_q_len": [len(f.get("question","")) for f in faqs[:3]] if faqs else [],
        "faq_a_len": [len(f.get("answer","")) for f in faqs[:3]] if faqs else [],
    })

for r in results:
    print(f"\n--- [{r['i']}] {r['slug']} ---")
    print(f"  title: {r['title']}")
    print(f"  words={r['words']} imgs={r['imgs']} h1={r['h1']} h2={r['h2']} h3={r['h3']}")
    print(f"  intro={r['has_intro']} conclusion={r['has_conclusion']}")
    print(f"  faqs={r['faq_count']} q_lens={r['faq_q_len']} a_lens={r['faq_a_len']}")
