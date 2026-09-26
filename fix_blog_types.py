filepath = 'app/blog/page.tsx'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复类型错误 - 添加所有必要的字段
old_code = '''<BlogListClient posts={allPosts.map(({ slug, title, excerpt, category, author, publishedAt, readTime, featured, image }) => ({ slug, title, excerpt, category, author, publishedAt, readTime, featured, image }))} />'''

new_code = '''<BlogListClient posts={allPosts.map(({ slug, title, excerpt, category, categorySlug, tags, author, publishedAt, readTime, featured, image }) => ({ slug, title, excerpt, category, categorySlug, tags, author, publishedAt, readTime, featured, image }))} />'''

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✓ Fixed TypeScript type error - added categorySlug and tags")
else:
    print("✗ Could not find the code block")
    # 尝试查找当前的代码
    import re
    match = re.search(r'<BlogListClient posts=\{[^}]+\} />', content)
    if match:
        print(f"Found: {match.group()[:100]}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nType fix complete!")
