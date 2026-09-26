"""Fix remaining rendered Chinese strings"""

# Fix 1: app/blog/tag/[slug]/page.tsx
with open('app/blog/tag/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('← ReturnBlog列Table', '← Back to Blog')
content = content.replace('Tags：#{tagName}', 'Tags: #{tagName}')
content = content.replace('{/* Tags标题 */}', '{/* Tags title */}')
content = content.replace('{/* 文章列Table */}', '{/* Article list */}')

with open('app/blog/tag/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("[OK] Fixed app/blog/tag/[slug]/page.tsx")

# Fix 2: components/theme/ThemeToggle.tsx
with open('components/theme/ThemeToggle.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('当前: ${theme === "light" ? "Light" : theme === "dark" ? "Dark" : "System"}',
                          'Current: ${theme === "light" ? "Light" : theme === "dark" ? "Dark" : "System"}')

with open('components/theme/ThemeToggle.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("[OK] Fixed components/theme/ThemeToggle.tsx")

# Verify
import re
for fname in ['app/blog/tag/[slug]/page.tsx', 'components/theme/ThemeToggle.tsx']:
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    # Check for Chinese in JSX strings (not comments)
    has_chinese = False
    for line in c.split('\n'):
        s = line.strip()
        if s.startswith('//') or s.startswith('*') or s.startswith('/*'):
            continue
        if re.search(r'[\u4e00-\u9fff]', line):
            print(f"  REMAINING in {fname}: {line.strip()[:80]}")
            has_chinese = True
    if not has_chinese:
        print(f"  [CLEAN] {fname}")
