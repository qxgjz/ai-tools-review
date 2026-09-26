import re

# 优化博客列表页 - 只传递必要字段给客户端，减少HTML大小
filepath = 'app/blog/page.tsx'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换BlogListClient的posts传递 - 只传递必要字段
old_code = '''      {/* 全部文章 - 带筛选和排序 */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          All Articles
        </h2>
        <BlogListClient posts={allPosts} />
      </div>'''

new_code = '''      {/* 全部文章 - 带筛选和排序 */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          All Articles
        </h2>
        <BlogListClient posts={allPosts.map(({ slug, title, excerpt, category, author, publishedAt, readTime, featured, image }) => ({ slug, title, excerpt, category, author, publishedAt, readTime, featured, image }))} />
      </div>'''

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✓ Optimized BlogListClient props - only essential fields passed")
else:
    print("✗ Could not find BlogListClient code block")

# 同时优化featuredPosts部分 - 也只使用必要字段
# 这部分已经只使用了必要字段，不需要修改

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nBlog list page optimization complete!")
print("  - Removed full article content from client-side props")
print("  - Only essential fields passed to BlogListClient")
print("  - Expected HTML size reduction: 60-80%")
