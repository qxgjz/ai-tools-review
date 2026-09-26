import json
import re

# 读取文章数据
with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

print("=== Articles Missing FAQ Section ===\n")

missing_faq = []
for i, post in enumerate(posts):
    content = post.get('content', '')
    title = post.get('title', 'Untitled')
    slug = post.get('slug', 'unknown')

    # 检查是否有FAQ部分
    has_faq = bool(re.search(r'(FAQ|Frequently Asked|frequently asked)', content, re.IGNORECASE))

    if not has_faq:
        missing_faq.append((i, title, slug))
        print(f"{len(missing_faq)}. {title[:70]}")
        print(f"   Slug: {slug}")
        print()

print(f"\nTotal articles: {len(posts)}")
print(f"Articles missing FAQ: {len(missing_faq)}")
