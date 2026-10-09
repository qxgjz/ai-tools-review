"""Read 3 lowest articles' current content."""
import json, os
os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

posts = json.load(open("data/posts.json", "r", encoding="utf-8"))
slugs = [
    "midjourney-v7-vs-flux-2026",
    "chatgpt-vs-claude-2026-comparison",
    "claude-37-vs-gpt4o",
]
for slug in slugs:
    p = next((x for x in posts if x["slug"] == slug), None)
    if not p:
        print(f"!! NOT FOUND: {slug}")
        continue
    print("=" * 80)
    print(f"SLUG: {slug}")
    print(f"TITLE: {p['title']}")
    print(f"WC: {p['wordCount']}, screenshots: {p.get('screenshotCount')}, faq: {len(p.get('faq', []))}")
    print(f"HAS quickAnswer: {bool(p.get('quickAnswer'))}")
    print(f"CONTENT (first 1500 chars):")
    print(p["content"][:1500])
    print("...")
    print(f"CONTENT (last 800 chars):")
    print(p["content"][-800:])
    print()
