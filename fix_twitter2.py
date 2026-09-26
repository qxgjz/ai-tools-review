blog_slug_path = r"app\blog\[slug]\page.tsx"
with open(blog_slug_path, "r", encoding="utf-8") as f:
    content = f.read()

old_twitter = """    twitter: {
      card: "summary_large_image",
      title: post.title.length > 60 ? post.title.slice(0, 57) + "..." : post.title,
      description: description,
    },"""

new_twitter = """    twitter: {
      card: "summary_large_image",
      title: post.title.length > 60 ? post.title.slice(0, 57) + "..." : post.title,
      description: description,
      images: [
        `https://www.aitoolcrux.com/api/og?title=${encodeURIComponent(post.title.slice(0, 50))}&description=${encodeURIComponent(description.slice(0, 100))}&category=${encodeURIComponent(post.category || "AI Tools")}`,
      ],
    },"""

if old_twitter in content:
    content = content.replace(old_twitter, new_twitter)
    with open(blog_slug_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("FIXED: Added twitter images to blog/[slug]/page.tsx")
else:
    print("SKIP: twitter block not found exactly")
