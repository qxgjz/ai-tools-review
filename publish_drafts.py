"""Publish all [READY] drafts to posts.json."""
import json
import os
import re
import shutil
from datetime import datetime

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
DRAFTS_DIR = os.path.join(PROJECT, "content_drafts")
PUBLISHED_DIR = os.path.join(DRAFTS_DIR, "published")
POSTS_FILE = os.path.join(PROJECT, "data", "posts.json")

os.makedirs(PUBLISHED_DIR, exist_ok=True)

with open(POSTS_FILE, "r", encoding="utf-8-sig") as f:
    posts = json.load(f)

existing_slugs = {p["slug"] for p in posts}
published = []

for fname in sorted(os.listdir(DRAFTS_DIR)):
    if not fname.endswith("_READY.md"):
        continue

    fpath = os.path.join(DRAFTS_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", fname.replace("_READY.md", ""))

    if slug in existing_slugs:
        print(f"  SKIP (already exists): {slug}")
        continue

    title_m = re.search(r"^#\s+(.+)$", content, re.M)
    title = title_m.group(1).strip() if title_m else slug.replace("-", " ").title()

    cat_m = re.search(r"\*\*Category:\*\*\s*(.+?)$", content, re.M)
    category = cat_m.group(1).strip() if cat_m else "AI Tools"

    date_m = re.search(r"\*\*Date:\*\*\s*(.+?)$", content, re.M)
    post_date = date_m.group(1).strip() if date_m else "2026-09-16"
    if "T" not in post_date:
        post_date = f"{post_date}T00:00:00.000000"

    tags = []
    for tag_line in re.findall(r"\*\*Tags?:\*\*\s*(.+?)$", content, re.M):
        tags = [t.strip() for t in re.split(r"[,,]", tag_line) if t.strip()]
    if not tags:
        tags = [w.title() for w in slug.replace("-", " ").split() if len(w) > 3][:5]

    words = len(re.sub(r"[#*_`\-\[\]()|>]", " ", content).split())
    reading_time = f"{max(1, round(words / 200))} min read"

    cat_slug_map = {
        "AI Chatbots": "chat", "AI Tools": "tools", "AI Agents": "agent",
        "AI Writing": "writing", "AI Image": "image", "AI Video": "video",
        "AI Productivity": "productivity", "AI Design": "design",
        "AI Search": "search", "AI Coding": "coding",
    }
    category_slug = cat_slug_map.get(category, "tools")

    excerpt_m = re.search(r"## Quick Answer\s*\n+(.+?)(?:\n---|\n##)", content, re.S)
    if excerpt_m:
        excerpt = re.sub(r"[*_`]", "", excerpt_m.group(1)).strip()[:150]
    else:
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip() and not p.startswith("#") and not p.startswith("**")]
        excerpt = paragraphs[0][:150] if paragraphs else title

    post = {
        "slug": slug,
        "title": title,
        "excerpt": excerpt,
        "date": post_date,
        "category": category,
        "categorySlug": category_slug,
        "author": "AIToolCrux Team",
        "readingTime": reading_time,
        "wordCount": words,
        "tags": tags,
        "hasRealScreenshots": False,
        "screenshotCount": 0,
        "content": content,
    }

    posts.insert(0, post)
    existing_slugs.add(slug)
    published.append(slug)
    print(f"  PUBLISHED: {slug} ({words} words)")
    shutil.move(fpath, os.path.join(PUBLISHED_DIR, fname))

with open(POSTS_FILE, "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print(f"\nTotal published: {len(published)}")
print(f"Total posts now: {len(posts)}")
