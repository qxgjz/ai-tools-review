"""Read FULL content of 3 articles to plan edits."""
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
    print("=" * 80)
    print(f"SLUG: {slug}  | wc={p['wordCount']}")
    print("FULL CONTENT:")
    print(p["content"])
    print()
