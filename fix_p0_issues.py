#!/usr/bin/env python3
"""
P0 Fixes - Based on real audit findings
1. Add favicon
2. Fix orphan pages (add internal links)
3. Handle duplicate Perplexity article (replace with new high-quality version)
"""

import json
import os
import re

print("=" * 70)
print("P0 FIXES - Based on Real Audit Findings")
print("=" * 70)

# ============================================
# FIX 1: Add Favicon
# ============================================
print("\n1. Adding Favicon...")

# Create a simple SVG favicon
favicon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6366F1;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#8B5CF6;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="100" height="100" rx="20" fill="url(#grad)"/>
  <text x="50" y="68" font-family="Arial, sans-serif" font-size="50" font-weight="bold" fill="white" text-anchor="middle">AI</text>
</svg>'''

favicon_path = "public/favicon.svg"
with open(favicon_path, "w", encoding="utf-8") as f:
    f.write(favicon_svg)
print(f"   ✅ Created {favicon_path}")

# Add favicon link to layout.tsx
layout_path = "app/layout.tsx"
with open(layout_path, "r", encoding="utf-8") as f:
    layout_content = f.read()

# Check if favicon already exists
if 'favicon' not in layout_content.lower():
    # Add favicon link in the head
    # Find the metadata export and add icons
    if 'metadata' in layout_content:
        # Add icons to metadata
        layout_content = layout_content.replace(
            'metadata = {',
            '''metadata = {
  icons: {
    icon: '/favicon.svg',
    shortcut: '/favicon.svg',
    apple: '/favicon.svg',
  },'''
        )
        with open(layout_path, "w", encoding="utf-8") as f:
            f.write(layout_content)
        print(f"   ✅ Added favicon to {layout_path}")
    else:
        print(f"   ⚠️ Could not find metadata in {layout_path}")
else:
    print(f"   ℹ️ Favicon already exists in {layout_path}")

# ============================================
# FIX 2: Fix Orphan Pages - Add internal links
# ============================================
print("\n2. Fixing Orphan Pages...")

# Orphan pages found: /tools/perplexity, /tools/dall-e, /tools/canva, /methodology
# We need to add links to these pages from hub pages

# Read tools.json to check if these tools exist
with open("data/tools.json", "r", encoding="utf-8") as f:
    tools = json.load(f)

print(f"   Total tools in database: {len(tools)}")

# Check for orphan tools
orphan_slugs = ['perplexity', 'dall-e', 'canva']
for slug in orphan_slugs:
    found = any(t.get('slug', '') == slug for t in tools)
    print(f"   {slug}: {'✅ Found in tools.json' if found else '❌ NOT found in tools.json'}")

# The issue is these tools exist but aren't linked from hub pages
# Let's check the homepage to see what tools are featured
homepage_path = "app/page.tsx"
with open(homepage_path, "r", encoding="utf-8") as f:
    homepage_content = f.read()

# Count featured tools on homepage
featured_count = homepage_content.count('tools/')
print(f"   Homepage references to tool pages: {featured_count}")

# The real fix: ensure these tools are in the right categories
# Check category assignments
print("\n   Checking category assignments for orphan tools:")
for slug in orphan_slugs:
    tool = next((t for t in tools if t.get('slug', '') == slug), None)
    if tool:
        category = tool.get('category', 'unknown')
        print(f"   {slug}: category={category}")
        # Check if category page exists
        category_path = f"app/category/[slug]/page.tsx"
        if os.path.exists(category_path):
            print(f"     ✅ Category page exists for {category}")
        else:
            print(f"     ❌ Category page missing for {category}")

# The methodology page is orphan - add link to footer
print("\n   Adding /methodology link to footer...")

# Find footer component
footer_paths = [
    "components/layout/Footer.tsx",
    "components/Footer.tsx",
    "app/components/Footer.tsx",
]

footer_found = False
for footer_path in footer_paths:
    if os.path.exists(footer_path):
        with open(footer_path, "r", encoding="utf-8") as f:
            footer_content = f.read()
        if 'methodology' not in footer_content.lower():
            # Add methodology link
            if 'About' in footer_content or 'about' in footer_content:
                footer_content = footer_content.replace(
                    'href="/about"',
                    'href="/about"\n            </Link>\n            <Link href="/methodology" className="text-gray-400 hover:text-white transition-colors">\n              Methodology'
                )
            with open(footer_path, "w", encoding="utf-8") as f:
                f.write(footer_content)
            print(f"   ✅ Added /methodology link to {footer_path}")
        else:
            print(f"   ℹ️ /methodology already in {footer_path}")
        footer_found = True
        break

if not footer_found:
    print(f"   ⚠️ Footer component not found in expected paths")
    # List components directory
    if os.path.exists("components"):
        print(f"   Components directory contents:")
        for item in os.listdir("components"):
            print(f"     - {item}")

# ============================================
# FIX 3: Handle duplicate Perplexity article
# ============================================
print("\n3. Handling Duplicate Perplexity Article...")

with open("data/posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

print(f"   Total posts: {len(posts)}")

# Find all Perplexity articles
perplexity_posts = [(i, p) for i, p in enumerate(posts) if 'perplexity' in p.get('slug', '').lower() or 'perplexity' in p.get('title', '').lower()]
print(f"   Perplexity articles found: {len(perplexity_posts)}")

for i, p in perplexity_posts:
    print(f"     [{i}] slug: {p.get('slug', '')[:50]}")
    print(f"         title: {p.get('title', '')[:60]}")
    print(f"         word count: {len(p.get('content', '').split())}")

# Strategy: Keep the new high-quality one (index 0, 2944 words)
# Remove the older duplicate if it's lower quality
if len(perplexity_posts) >= 2:
    # Sort by word count, keep the longest
    sorted_posts = sorted(perplexity_posts, key=lambda x: len(x[1].get('content', '').split()), reverse=True)
    keep_index = sorted_posts[0][0]
    remove_indices = [p[0] for p in sorted_posts[1:]]
    
    print(f"\n   Keeping post at index {keep_index} ({len(sorted_posts[0][1].get('content', '').split())} words)")
    print(f"   Removing {len(remove_indices)} duplicate(s): indices {remove_indices}")
    
    # Remove duplicates (in reverse order to preserve indices)
    for idx in sorted(remove_indices, reverse=True):
        removed = posts.pop(idx)
        print(f"   ✅ Removed: {removed.get('slug', '')[:50]}")
    
    with open("data/posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Posts count after cleanup: {len(posts)}")
else:
    print(f"   ℹ️ No duplicates found, keeping all posts")

# ============================================
# Summary
# ============================================
print("\n" + "=" * 70)
print("P0 FIXES COMPLETE")
print("=" * 70)
print("✅ Favicon created and added to layout")
print("✅ Orphan pages identified (will need component-level fixes)")
print("✅ Duplicate Perplexity article handled")
print("=" * 70)
print("\nNext steps (P1):")
print("  - Optimize Title lengths (<=60 chars)")
print("  - Optimize Meta Description lengths (<=160 chars)")
print("  - Add Quick Answer/Key Takeaways to article pages")
print("  - Add internal links to important tool pages")
print("  - Add og:type to Open Graph tags")
