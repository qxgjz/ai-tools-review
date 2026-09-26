"""Check FAQ section HTML content and FAQPage schema presence."""
import json
import re
from pathlib import Path

POSTS = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\data\posts.json")
with open(POSTS, "r", encoding="utf-8") as f:
    posts = json.load(f)

n = len(posts)
idxs = [int(i * n / 10) for i in range(10)]
sample = [posts[i] for i in idxs]

print("=== FAQ section content extraction ===")
for i, p in enumerate(sample):
    content = p.get("content", "") or ""
    # Find FAQ section
    m = re.search(r'(?is)(<h2[^>]*>[^<]*(?:faq|frequently asked)[^<]*</h2>.*?)(?=<h2|$)', content)
    if m:
        faq_html = m.group(1)
        # Count questions (h3 or strong or p with question mark)
        qs = re.findall(r'(?is)(<h3[^>]*>.*?</h3>|<strong>[^<]*\?</strong>)', faq_html)
        print(f"[{i}] {p.get('slug','?')[:45]}: FAQ section found, ~{len(qs)} questions")
        # Show first question
        if qs:
            q_text = re.sub(r"<[^>]+>", "", qs[0]).strip()[:80]
            print(f"    Q1: {q_text}")
    else:
        print(f"[{i}] {p.get('slug','?')[:45]}: NO FAQ section in content")

print("\n=== Summary stats across all 105 posts ===")
no_faq = 0; no_img = 0; too_long = 0; no_h1 = 0; has_faq_schema = 0
for p in posts:
    c = p.get("content", "") or ""
    if not re.search(r'(?i)(faq|frequently asked)', c): no_faq += 1
    if not re.search(r"<img", c): no_img += 1
    text = re.sub(r"<[^>]+>", " ", c)
    w = len(re.findall(r"\b\w+\b", text))
    if w > 2000: too_long += 1
    if not re.search(r"<h1", c): no_h1 += 1
print(f"  Posts without FAQ section: {no_faq}/105")
print(f"  Posts without any <img>: {no_img}/105")
print(f"  Posts over 2000 words: {too_long}/105")
print(f"  Posts without H1 in content: {no_h1}/105")
