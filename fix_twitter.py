import json
import os

# Fix 1: Add missing twitter:card and twitter:image to blog [slug] page metadata
blog_slug_path = r"app\blog\[slug]\page.tsx"
with open(blog_slug_path, "r", encoding="utf-8") as f:
    content = f.read()

# Check if openGraph block exists and add twitter after it
# Find the openGraph closing and add twitter before alternates
old_og_close = """      openGraph: {
        title: `${post.title} | AIToolCrux`,
        description: post.excerpt,
        type: "article",
        publishedTime: post.date || post.publishedAt,
        modifiedTime: post.date || post.publishedAt,
        authors: ["AIToolCrux"],
        images: [
          {
            url: `/api/og?title=${encodeURIComponent(post.title)}&description=${encodeURIComponent(post.excerpt || '')}&category=${encodeURIComponent(post.category || 'AI Tools')}`,
            width: 1200,
            height: 630,
            alt: post.title,
          },
        ],
      },"""

new_og_close = """      openGraph: {
        title: `${post.title} | AIToolCrux`,
        description: post.excerpt,
        type: "article",
        publishedTime: post.date || post.publishedAt,
        modifiedTime: post.date || post.publishedAt,
        authors: ["AIToolCrux"],
        images: [
          {
            url: `/api/og?title=${encodeURIComponent(post.title)}&description=${encodeURIComponent(post.excerpt || '')}&category=${encodeURIComponent(post.category || 'AI Tools')}`,
            width: 1200,
            height: 630,
            alt: post.title,
          },
        ],
      },
      twitter: {
        card: "summary_large_image",
        title: `${post.title} | AIToolCrux`,
        description: post.excerpt,
        images: [
          `/api/og?title=${encodeURIComponent(post.title)}&description=${encodeURIComponent(post.excerpt || '')}&category=${encodeURIComponent(post.category || 'AI Tools')}`,
        ],
      },"""

if old_og_close in content:
    content = content.replace(old_og_close, new_og_close)
    with open(blog_slug_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("FIXED: Added twitter:card and twitter:image to blog/[slug]/page.tsx")
else:
    print("SKIP: Could not find exact openGraph block in blog/[slug]/page.tsx")
    # Try to find what's actually there
    if "openGraph:" in content:
        idx = content.index("openGraph:")
        print(f"  Found openGraph at position {idx}")
        print(f"  Context: {content[idx:idx+200]}")

# Fix 2: Also add date field to the 5 posts that only have publishedAt
posts_path = "data/posts.json"
with open(posts_path, "r", encoding="utf-8") as f:
    posts = json.load(f)

fixed = 0
for post in posts:
    if "date" not in post and "publishedAt" in post:
        post["date"] = post["publishedAt"]
        fixed += 1

if fixed > 0:
    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"FIXED: Added 'date' field to {fixed} posts (copied from publishedAt)")
else:
    print("SKIP: No posts need date field fix")

print("\nDone!")
