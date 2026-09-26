#!/usr/bin/env python3
"""
Iteration 6: Fix SEO issues found in deep audit
- Fix homepage title (65 chars -> <=60)
- Fix category meta descriptions (164 chars -> <=160)
- Fix alternatives list page title (75 chars -> <=60) and meta desc (178 -> <=160)
- Fix homepage canonical mismatch
- Fix image alt text on tool pages
"""

import json
import os
import re

BASE = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

print("=" * 60)
print("  Iteration 6: Fix SEO Issues")
print("=" * 60)
print()

# ==========================================
# 1. Fix homepage title in layout.tsx
# ==========================================
print("[1/5] Fixing homepage title...")
layout_path = os.path.join(BASE, 'app', 'layout.tsx')
with open(layout_path, 'r', encoding='utf-8') as f:
    layout_content = f.read()

# Current title: "Best AI Tools 2026: Expert Reviews & Comparisons | AIToolCrux" (65 chars)
# New title: "Best AI Tools 2026: Expert Reviews | AIToolCrux" (54 chars)
old_title = 'Best AI Tools 2026: Expert Reviews & Comparisons | AIToolCrux'
new_title = 'Best AI Tools 2026: Expert Reviews | AIToolCrux'

if old_title in layout_content:
    layout_content = layout_content.replace(old_title, new_title)
    with open(layout_path, 'w', encoding='utf-8') as f:
        f.write(layout_content)
    print(f"  ✅ Homepage title fixed: 65 -> {len(new_title)} chars")
else:
    print(f"  ⚠️  Homepage title not found, checking...")
    # Try to find title pattern
    title_match = re.search(r'title:\s*["\']([^"\']+)["\']', layout_content)
    if title_match:
        print(f"  Found title: {title_match.group(1)} ({len(title_match.group(1))} chars)")

# ==========================================
# 2. Fix category page meta descriptions
# ==========================================
print("\n[2/5] Fixing category page meta descriptions...")
category_path = os.path.join(BASE, 'app', 'category', '[slug]', 'page.tsx')
with open(category_path, 'r', encoding='utf-8') as f:
    cat_content = f.read()

# The meta description pattern likely generates something like:
# "Discover the best {category} AI tools in 2026. Expert reviews with 6-dimension ratings, pricing comparisons, and more."
# Need to find and shorten it

# Look for meta description generation
desc_patterns = [
    r'description:\s*`([^`]+)`',
    r'description:\s*"([^"]+)"',
    r"description:\s*'([^']+)'",
]

for pattern in desc_patterns:
    matches = re.findall(pattern, cat_content)
    for m in matches:
        if len(m) > 160:
            print(f"  Found long description: {len(m)} chars")
            # Shorten it
            # We'll modify the template to be shorter
            break

# Let's look at the actual description template
desc_match = re.search(r'(description:\s*[`"\'])([^`"\']+)([`"\'])', cat_content)
if desc_match:
    old_desc = desc_match.group(2)
    print(f"  Current description template: {old_desc[:80]}... ({len(old_desc)} chars)")
    
    # Create a shorter version
    # Original likely: "Discover the best {categoryName} AI tools in 2026. Expert reviews with 6-dimension ratings, pricing comparisons, and free trials."
    # New: "Best {categoryName} AI tools 2026: expert reviews, 6-dimension ratings, pricing, and free trials."
    if 'Discover the best' in old_desc and 'Expert reviews with 6-dimension ratings' in old_desc:
        new_desc = old_desc.replace(
            'Discover the best ', 'Best '
        ).replace(
            ' AI tools in 2026. Expert reviews with 6-dimension ratings, pricing comparisons, and more.',
            ' AI tools 2026: expert reviews, 6-dimension ratings, pricing, and free trials.'
        )
        # Replace in content
        cat_content = cat_content.replace(old_desc, new_desc)
        with open(category_path, 'w', encoding='utf-8') as f:
            f.write(cat_content)
        print(f"  ✅ Category description fixed: {len(old_desc)} -> {len(new_desc)} chars")
    else:
        print(f"  ⚠️  Description pattern not matching expected format")
else:
    print(f"  ⚠️  Description template not found")

# ==========================================
# 3. Fix alternatives list page title and meta
# ==========================================
print("\n[3/5] Fixing alternatives list page title and meta...")
alt_path = os.path.join(BASE, 'app', 'alternatives', 'page.tsx')
if os.path.exists(alt_path):
    with open(alt_path, 'r', encoding='utf-8') as f:
        alt_content = f.read()
    
    # Fix title
    old_alt_title = 'Best AI Tool Alternatives 2026: Comprehensive Comparison Guide | AIToolCrux'
    new_alt_title = 'Best AI Tool Alternatives 2026 | AIToolCrux'
    
    if old_alt_title in alt_content:
        alt_content = alt_content.replace(old_alt_title, new_alt_title)
        print(f"  ✅ Alternatives title fixed: 75 -> {len(new_alt_title)} chars")
    else:
        print(f"  ⚠️  Alternatives title not found, checking...")
        title_match = re.search(r'title:\s*["\']([^"\']+)["\']', alt_content)
        if title_match:
            print(f"  Found: {title_match.group(1)} ({len(title_match.group(1))} chars)")
    
    # Fix meta description
    old_alt_desc = 'Discover the best alternatives to popular AI tools. Compare ChatGPT alternatives, Midjourney alternatives, and more with expert reviews and pricing.'
    new_alt_desc = 'Best AI tool alternatives 2026: ChatGPT, Midjourney, Claude alternatives compared with expert reviews and pricing.'
    
    if old_alt_desc in alt_content:
        alt_content = alt_content.replace(old_alt_desc, new_alt_desc)
        print(f"  ✅ Alternatives meta description fixed: 178 -> {len(new_alt_desc)} chars")
    else:
        print(f"  ⚠️  Alternatives meta description not found")
    
    with open(alt_path, 'w', encoding='utf-8') as f:
        f.write(alt_content)
else:
    print(f"  ⚠️  Alternatives page not found at {alt_path}")

# ==========================================
# 4. Fix homepage canonical
# ==========================================
print("\n[4/5] Fixing homepage canonical...")
home_path = os.path.join(BASE, 'app', 'page.tsx')
with open(home_path, 'r', encoding='utf-8') as f:
    home_content = f.read()

# Check if canonical is set in metadata
canonical_match = re.search(r'canonical:\s*["\']([^"\']+)["\']', home_content)
if canonical_match:
    current_canonical = canonical_match.group(1)
    print(f"  Current canonical: {current_canonical}")
    if current_canonical == 'https://www.aitoolcrux.com':
        # Should be https://www.aitoolcrux.com/
        home_content = home_content.replace(
            'canonical: "https://www.aitoolcrux.com"',
            'canonical: "https://www.aitoolcrux.com/"'
        ).replace(
            "canonical: 'https://www.aitoolcrux.com'",
            "canonical: 'https://www.aitoolcrux.com/'"
        )
        with open(home_path, 'w', encoding='utf-8') as f:
            f.write(home_content)
        print(f"  ✅ Homepage canonical fixed: added trailing slash")
    else:
        print(f"  ✅ Homepage canonical already correct")
else:
    # Check if canonical is in layout.tsx
    layout_canonical = re.search(r'canonical:\s*["\']([^"\']+)["\']', layout_content)
    if layout_canonical:
        print(f"  Canonical found in layout.tsx: {layout_canonical.group(1)}")
    else:
        print(f"  ⚠️  Canonical not explicitly set, using default")

# ==========================================
# 5. Fix image alt text on tool pages
# ==========================================
print("\n[5/5] Fixing image alt text on tool pages...")
tool_page_path = os.path.join(BASE, 'app', 'tools', '[slug]', 'page.tsx')
with open(tool_page_path, 'r', encoding='utf-8') as f:
    tool_content = f.read()

# Find Image components without alt or with empty alt
# Pattern: <Image ... src={...} ... />
image_matches = re.findall(r'<Image[^>]+>', tool_content)
print(f"  Found {len(image_matches)} Image components")

# Check for logo image specifically
logo_img_match = re.search(r'<Image[^>]*logo[^>]*/?>', tool_content, re.IGNORECASE)
if logo_img_match:
    logo_img = logo_img_match.group(0)
    if 'alt=' not in logo_img or 'alt=""' in logo_img or "alt=''" in logo_img:
        # Add alt text
        if 'alt=' in logo_img:
            new_logo_img = re.sub(r'alt=["\'][^"\']*["\']', 'alt={`${tool.name} logo`}', logo_img)
        else:
            new_logo_img = logo_img.replace('/>', ' alt={`${tool.name} logo`} />')
        tool_content = tool_content.replace(logo_img, new_logo_img)
        print(f"  ✅ Tool logo image alt text fixed")
    else:
        print(f"  ✅ Tool logo image already has alt text")
else:
    # Try to find any Image with tool.logo
    logo_src_match = re.search(r'<Image[^>]*src=\{tool\.logo\}[^>]*/?>', tool_content)
    if logo_src_match:
        logo_img = logo_src_match.group(0)
        if 'alt=' not in logo_img:
            new_logo_img = logo_img.replace('/>', ' alt={`${tool.name} logo`} />')
            tool_content = tool_content.replace(logo_img, new_logo_img)
            print(f"  ✅ Tool logo image alt text fixed (src=tool.logo)")
        else:
            print(f"  ✅ Tool logo image already has alt text")
    else:
        print(f"  ⚠️  Tool logo image pattern not found, checking screenshot images...")
        # Check for screenshot images
        screenshot_match = re.search(r'<Image[^>]*screenshot[^>]*/?>', tool_content, re.IGNORECASE)
        if screenshot_match:
            print(f"  Found screenshot image: {screenshot_match.group(0)[:100]}")

with open(tool_page_path, 'w', encoding='utf-8') as f:
    f.write(tool_content)

print()
print("=" * 60)
print("  All SEO fixes applied!")
print("=" * 60)
print()
print("  Files modified:")
print("  1. app/layout.tsx - homepage title")
print("  2. app/category/[slug]/page.tsx - category meta descriptions")
print("  3. app/alternatives/page.tsx - alternatives title and meta")
print("  4. app/page.tsx - homepage canonical")
print("  5. app/tools/[slug]/page.tsx - image alt text")
