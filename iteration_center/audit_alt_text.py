import json, re

with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

no_alt = 0
missing_alt_posts = []
total_imgs = 0
for p in posts:
    content = p.get('content', '')
    imgs = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
    total_imgs += len(imgs)
    for img in imgs:
        alt_match = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', img, re.IGNORECASE)
        if not alt_match or not alt_match.group(1).strip():
            no_alt += 1
            if p['slug'] not in missing_alt_posts:
                missing_alt_posts.append(p['slug'])

print(f'Total posts: {len(posts)}')
print(f'Total images: {total_imgs}')
print(f'Images missing alt text: {no_alt}')
print(f'Posts with missing alt: {len(missing_alt_posts)}')
for s in missing_alt_posts[:15]:
    print(f'  - {s}')

with_screenshots = sum(1 for p in posts if p.get('screenshotCount', 0) > 0 or p.get('hasRealScreenshots'))
print(f'\nPosts with screenshots: {with_screenshots}')

# Also check tool page images
with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)
print(f'\nTotal tools: {len(tools)}')
