import json

posts = json.load(open("data/posts.json", "r", encoding="utf-8"))
missing = [p for p in posts if "date" not in p and "publishedAt" not in p]
print(f"Posts missing both date and publishedAt: {len(missing)}")
for p in missing[:5]:
    print(f"  - {p['slug']}")

no_date = [p for p in posts if "date" not in p and "publishedAt" in p]
print(f"\nPosts with publishedAt but no date: {len(no_date)}")
for p in no_date[:5]:
    print(f"  - {p['slug']}: publishedAt={p.get('publishedAt','N/A')}")

# Check for missing twitter image in blog metadata
print("\n--- Checking blog page metadata ---")
with open("app/blog/[slug]/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()
if "twitter:image" in content:
    print("twitter:image: FOUND")
else:
    print("twitter:image: MISSING")
if "twitter:card" in content:
    print("twitter:card: FOUND")
else:
    print("twitter:card: MISSING")
