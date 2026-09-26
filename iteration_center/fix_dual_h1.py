"""Fix double H1 issues in blog posts:
1. Find posts with embedded <h1> in content -> change to <h2>
2. Find chatgpt-vs-claude duplicate meta description issue
"""
import json
import re
import sys

PROJ = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"

# Load posts
with open(f"{PROJ}\\data\\posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

print(f"Total posts: {len(posts)}")

# 1. Find posts with embedded <h1> in content
h1_posts = []
for p in posts:
    content = p.get("content", "")
    h1_count = len(re.findall(r"<h1[ >]", content, re.I))
    if h1_count > 0:
        h1_posts.append(p)

print(f"\nPosts with embedded <h1> in content: {len(h1_posts)}")
for p in h1_posts:
    print(f"  - {p['slug']}")

# 2. Fix: change <h1> to <h2> in content (but not the first one if it's a title)
# The blog template already renders the title as <h1>, so any <h1> in content should be <h2>
fixed_count = 0
for p in h1_posts:
    content = p["content"]
    # Replace <h1 ...>...</h1> with <h2 ...>...</h2>
    new_content = re.sub(r"<h1([^>]*)>", r"<h2\1>", content, flags=re.I)
    new_content = re.sub(r"</h1>", "</h2>", new_content, flags=re.I)
    if new_content != content:
        p["content"] = new_content
        fixed_count += 1

print(f"\nFixed {fixed_count} posts (h1 -> h2 in content)")

# 3. Find chatgpt-vs-claude duplicate
print("\n--- ChatGPT vs Claude posts ---")
for p in posts:
    if "chatgpt-vs-claude" in p.get("slug", "").lower():
        print(f"  Slug: {p['slug']}")
        print(f"  Title: {p.get('title','')}")
        print(f"  Excerpt: {p.get('excerpt','')[:120]}")
        print()

# Save posts back
with open(f"{PROJ}\\data\\posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print("posts.json saved.")
