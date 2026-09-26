#!/usr/bin/env python3
"""
Iteration 1: Fix Title and Meta Description lengths
Based on real SEO audit findings
- Tool pages: 67-70 chars -> target <=60
- Category pages: 61 chars -> target <=60
- Article pages: up to 91 chars -> target <=60
- Alternatives pages: up to 75 chars -> target <=60
- Meta descriptions: up to 326 chars -> target <=160
"""

import re
import json
import os

print("=" * 70)
print("ITERATION 1: Fix Title & Meta Description Lengths")
print("=" * 70)

changes_made = []

# ============================================
# FIX 1: Tool detail page title (533 pages affected)
# ============================================
print("\n1. Fixing tool detail page titles...")

tool_page_path = "app/tools/[slug]/page.tsx"
with open(tool_page_path, "r", encoding="utf-8") as f:
    content = f.read()

# Old title template (67-70 chars)
old_tool_title = 'title: `${tool.name} Review 2026: ${total.toFixed(1)}/10 Rating, Pricing & Pros | AIToolCrux`,'
# New title template (~45-55 chars)
new_tool_title = 'title: `${tool.name} Review 2026: ${total.toFixed(1)}/10 | AIToolCrux`,'

if old_tool_title in content:
    content = content.replace(old_tool_title, new_tool_title)
    changes_made.append(f"Tool page title shortened: 'Rating, Pricing & Pros' removed")
    print(f"   ✅ Tool page title template updated")
else:
    print(f"   ⚠️ Old tool title pattern not found, checking...")
    # Try to find the actual line
    for i, line in enumerate(content.split('\n')):
        if 'Review 2026' in line and 'title:' in line:
            print(f"   Found at line {i+1}: {line.strip()[:80]}")

# Also fix OG and Twitter titles for tool pages
old_og_title = 'title: `${tool.name} Review 2026: ${total.toFixed(1)}/10 Rating, Pricing & Pros/Cons`,'
new_og_title = 'title: `${tool.name} Review 2026: ${total.toFixed(1)}/10 | AIToolCrux`,'

if old_og_title in content:
    content = content.replace(old_og_title, new_og_title)
    changes_made.append("Tool page OG/Twitter title shortened")
    print(f"   ✅ Tool page OG/Twitter title updated")

with open(tool_page_path, "w", encoding="utf-8") as f:
    f.write(content)

# ============================================
# FIX 2: Category page title (17 pages affected)
# ============================================
print("\n2. Fixing category page titles...")

cat_page_path = "app/category/[slug]/page.tsx"
with open(cat_page_path, "r", encoding="utf-8") as f:
    content = f.read()

old_cat_title = 'const title = `Best ${categoryName} AI Tools 2026: Top ${toolCount} Rated | AIToolCrux`;'
new_cat_title = 'const title = `Best ${categoryName} AI Tools: Top ${toolCount} Rated | AIToolCrux`;'

if old_cat_title in content:
    content = content.replace(old_cat_title, new_cat_title)
    changes_made.append("Category page title shortened: '2026' removed")
    print(f"   ✅ Category page title template updated")
else:
    print(f"   ⚠️ Old category title pattern not found")
    for i, line in enumerate(content.split('\n')):
        if 'Best' in line and 'AI Tools' in line and 'title' in line:
            print(f"   Found at line {i+1}: {line.strip()[:80]}")

with open(cat_page_path, "w", encoding="utf-8") as f:
    f.write(content)

# ============================================
# FIX 3: Article page titles - truncate if >60 chars (48 pages)
# ============================================
print("\n3. Fixing article page titles (truncate >60 chars)...")

blog_page_path = "app/blog/[slug]/page.tsx"
with open(blog_page_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add title truncation logic in generateMetadata
# Find the line: title: post.title,
old_blog_title = '    title: post.title,'
new_blog_title = '    title: post.title.length > 60 ? post.title.slice(0, 57) + "..." : post.title,'

if old_blog_title in content:
    content = content.replace(old_blog_title, new_blog_title)
    changes_made.append("Article page title truncated if >60 chars")
    print(f"   ✅ Article page title truncation added")
else:
    print(f"   ⚠️ Article title pattern not found")

# Also fix OG and Twitter titles for blog
old_blog_og = '      title: post.title,'
new_blog_og = '      title: post.title.length > 60 ? post.title.slice(0, 57) + "..." : post.title,'

count = content.count(old_blog_og)
if count > 0:
    content = content.replace(old_blog_og, new_blog_og)
    changes_made.append(f"Article OG/Twitter title truncated ({count} occurrences)")
    print(f"   ✅ Article OG/Twitter title truncation added ({count} occurrences)")

with open(blog_page_path, "w", encoding="utf-8") as f:
    f.write(content)

# ============================================
# FIX 4: Alternatives page titles - truncate if >60 chars (8 pages)
# ============================================
print("\n4. Fixing alternatives page titles (truncate >60 chars)...")

alt_page_path = "app/alternatives/[slug]/page.tsx"
with open(alt_page_path, "r", encoding="utf-8") as f:
    content = f.read()

old_alt_title = '    title: page.title,'
new_alt_title = '    title: page.title.length > 60 ? page.title.slice(0, 57) + "..." : page.title,'

if old_alt_title in content:
    content = content.replace(old_alt_title, new_alt_title)
    changes_made.append("Alternatives page title truncated if >60 chars")
    print(f"   ✅ Alternatives page title truncation added")
else:
    print(f"   ⚠️ Alternatives title pattern not found")

# Also fix OG and Twitter
old_alt_og = '      title: page.title,'
new_alt_og = '      title: page.title.length > 60 ? page.title.slice(0, 57) + "..." : page.title,'

count = content.count(old_alt_og)
if count > 0:
    content = content.replace(old_alt_og, new_alt_og)
    changes_made.append(f"Alternatives OG/Twitter title truncated ({count} occurrences)")
    print(f"   ✅ Alternatives OG/Twitter title truncation added ({count} occurrences)")

with open(alt_page_path, "w", encoding="utf-8") as f:
    f.write(content)

# ============================================
# FIX 5: Meta Description - ensure all <=160 chars
# ============================================
print("\n5. Fixing Meta Description lengths...")

# Check about page description
about_page_path = "app/about/page.tsx"
if os.path.exists(about_page_path):
    with open(about_page_path, "r", encoding="utf-8") as f:
        about_content = f.read()
    
    # Find description line
    desc_match = re.search(r'description:\s*["\'`](.+?)["\'`],', about_content)
    if desc_match:
        old_desc = desc_match.group(1)
        if len(old_desc) > 160:
            new_desc = old_desc[:157] + "..."
            about_content = about_content.replace(old_desc, new_desc)
            with open(about_page_path, "w", encoding="utf-8") as f:
                f.write(about_content)
            changes_made.append(f"About page description: {len(old_desc)} -> {len(new_desc)} chars")
            print(f"   ✅ About page description shortened: {len(old_desc)} -> {len(new_desc)} chars")
        else:
            print(f"   ℹ️ About page description already OK ({len(old_desc)} chars)")
    else:
        print(f"   ⚠️ About page description not found")

# Check methodology page
method_page_path = "app/methodology/page.tsx"
if os.path.exists(method_page_path):
    with open(method_page_path, "r", encoding="utf-8") as f:
        method_content = f.read()
    
    desc_match = re.search(r'description:\s*["\'`](.+?)["\'`],', method_content)
    if desc_match:
        old_desc = desc_match.group(1)
        if len(old_desc) > 160:
            new_desc = old_desc[:157] + "..."
            method_content = method_content.replace(old_desc, new_desc)
            with open(method_page_path, "w", encoding="utf-8") as f:
                f.write(method_content)
            changes_made.append(f"Methodology page description: {len(old_desc)} -> {len(new_desc)} chars")
            print(f"   ✅ Methodology page description shortened: {len(old_desc)} -> {len(new_desc)} chars")
        else:
            print(f"   ℹ️ Methodology page description already OK ({len(old_desc)} chars)")

# ============================================
# Summary
# ============================================
print("\n" + "=" * 70)
print("ITERATION 1 COMPLETE - Title & Meta Fixes")
print("=" * 70)
print(f"\nChanges made ({len(changes_made)}):")
for i, change in enumerate(changes_made, 1):
    print(f"  {i}. {change}")

print(f"\nPages affected:")
print(f"  - Tool detail pages: 533 (title template)")
print(f"  - Category pages: 17 (title template)")
print(f"  - Article pages: 48 (title truncation)")
print(f"  - Alternatives pages: 8 (title truncation)")
print(f"  - About page: 1 (description)")
print(f"  - Methodology page: 1 (description)")
print(f"  Total: ~608 pages")

print(f"\nNext: TypeScript compilation check -> GitHub commit -> Vercel deploy -> Verify")
print("=" * 70)
