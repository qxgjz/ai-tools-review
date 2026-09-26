"""Find articles that fit the free AI tools guide"""
import json

with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

print(f"Total posts: {len(posts)}")
print()

# Find posts related to free tools, no credit card, etc.
free_keywords = ['free', 'no credit card', 'best free', 'without paying', 'zero cost', 'no cost', 'free tier', 'freemium']
for p in posts:
    title = p.get('title', '').lower()
    excerpt = p.get('excerpt', '').lower()
    tags = [t.lower() for t in p.get('tags', [])]
    
    score = 0
    for kw in free_keywords:
        if kw in title:
            score += 3
        if kw in excerpt:
            score += 1
        if any(kw in t for t in tags):
            score += 2
    
    if score > 0:
        print(f"[{score}] {p['title']}")
        print(f"    slug: {p['slug']}")
        print(f"    date: {p.get('date','')}")
        print()

# Also show all post titles to see what we have
print("=== All post titles ===")
for p in posts:
    print(f"  {p.get('title','?')} -> /blog/{p.get('slug','?')}")
