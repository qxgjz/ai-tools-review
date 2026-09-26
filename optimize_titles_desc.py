import re
import os

def optimize_file(filepath, optimizations):
    """优化文件中的title和description"""
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes_made = 0

    for old_text, new_text in optimizations:
        if old_text in content:
            content = content.replace(old_text, new_text)
            changes_made += 1
            print(f"  ✓ Replaced: {old_text[:50]}... -> {new_text[:50]}...")
        else:
            print(f"  ✗ Not found: {old_text[:50]}...")

    if changes_made > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {filepath}: {changes_made} changes made")
        return True
    else:
        print(f"  - {filepath}: no changes")
        return False

print("="*60)
print("OPTIMIZING TITLES AND META DESCRIPTIONS")
print("="*60)

# 1. 优化 layout.tsx - 全局description
print("\n1. app/layout.tsx")
optimize_file('app/layout.tsx', [
    (
        'Discover 500+ AI tools with expert 6-dimension reviews. Compare ChatGPT, Claude, Gemini and more. Find the perfect AI tool for your needs.',
        'Discover 500+ AI tools with expert 6-dimension reviews. Compare ChatGPT, Claude, Gemini and find your perfect AI tool.'
    ),
])

# 2. 优化首页 page.tsx - description
print("\n2. app/page.tsx")
optimize_file('app/page.tsx', [
    (
        'Professional AI tool reviews, comparisons, and recommendations based on a six-dimensional evaluation framework. Find the best AI tools for your workflow.',
        'Expert AI tool reviews and comparisons based on a six-dimensional evaluation framework. Find the best AI tools for your workflow.'
    ),
])

# 3. 优化排行页 - 需要检查ranking/layout.tsx
print("\n3. app/ranking/layout.tsx")
if os.path.exists('app/ranking/layout.tsx'):
    with open('app/ranking/layout.tsx', 'r', encoding='utf-8') as f:
        content = f.read()
    print("  Content preview:")
    print(content[:500])
else:
    print("  Not found, checking ranking/page.tsx metadata...")

# 4. 优化Methodology页
print("\n4. app/methodology/page.tsx")
optimize_file('app/methodology/page.tsx', [
    (
        'Learn how AIToolCrux evaluates AI tools with our transparent six-dimensional weighting system. Every tool undergoes standardized testing across features, quality, UX, pricing, support, and updates.',
        'Learn how AIToolCrux evaluates AI tools with our transparent six-dimensional system. Every tool undergoes standardized testing across features, quality, UX, pricing, and support.'
    ),
])

# 5. 优化About页
print("\n5. app/about/page.tsx")
optimize_file('app/about/page.tsx', [
    (
        'Learn about AIToolCrux',
        'AIToolCrux provides expert, unbiased AI tool reviews and comparisons. Our mission is to help you find the perfect AI tools with transparent, data-driven evaluations.'
    ),
])

# 6. 检查并优化工具详情页title模板
print("\n6. app/tools/[slug]/page.tsx - checking title template")
with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    tool_content = f.read()

# 查找title模板
title_pattern = r'title:\s*`([^`]+)`'
title_matches = re.findall(title_pattern, tool_content)
for t in title_matches:
    print(f"  Found title template: {t} ({len(t)} chars)")

# 优化工具详情页title - 缩短格式
if 'Review 2026:' in tool_content and 'Rating, Pricing & Pros/Cons' in tool_content:
    old_title = '${tool.name} Review 2026: ${total.toFixed(1)}/10 Rating, Pricing & Pros/Cons | AIToolCrux'
    new_title = '${tool.name} Review 2026: ${total.toFixed(1)}/10 Rating, Pricing & Pros | AIToolCrux'
    if old_title in tool_content:
        tool_content = tool_content.replace(old_title, new_title)
        with open('app/tools/[slug]/page.tsx', 'w', encoding='utf-8') as f:
            f.write(tool_content)
        print(f"  ✓ Optimized tool title template (removed '/Cons')")

# 7. 检查并优化分类页title模板
print("\n7. app/category/[slug]/page.tsx - checking title template")
with open('app/category/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    cat_content = f.read()

cat_title_matches = re.findall(title_pattern, cat_content)
for t in cat_title_matches:
    print(f"  Found title template: {t} ({len(t)} chars)")

# 优化分类页title - 缩短格式
if 'Best' in cat_content and 'AI Tools 2026:' in cat_content and 'Rated & Compared' in cat_content:
    old_cat_title = 'Best ${categoryName} AI Tools 2026: Top ${toolCount} Rated & Compared | AIToolCrux'
    new_cat_title = 'Best ${categoryName} AI Tools 2026: Top ${toolCount} Rated | AIToolCrux'
    if old_cat_title in cat_content:
        cat_content = cat_content.replace(old_cat_title, new_cat_title)
        with open('app/category/[slug]/page.tsx', 'w', encoding='utf-8') as f:
            f.write(cat_content)
        print(f"  ✓ Optimized category title template (removed '& Compared')")

print("\n" + "="*60)
print("TITLE AND DESCRIPTION OPTIMIZATION COMPLETE")
print("="*60)
