import os

files_to_check = [
    'app/tools/[slug]/page.tsx',
    'app/category/[slug]/page.tsx',
    'app/alternatives/[slug]/page.tsx',
    'app/ranking/page.tsx',
    'app/ranking/layout.tsx',
    'app/blog/page.tsx',
    'app/about/page.tsx',
    'app/methodology/page.tsx',
]

print('=== Checking Open Graph tags ===')
for filepath in files_to_check:
    if not os.path.exists(filepath):
        print(f'SKIP: {filepath} not found')
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_og_type = 'og:type' in content or '"type":' in content
    has_openGraph = 'openGraph' in content
    
    if has_openGraph and not has_og_type:
        print(f'FIX: {filepath} - has openGraph but missing og:type')
    elif has_openGraph and has_og_type:
        print(f'OK: {filepath} - has openGraph and og:type')
    else:
        print(f'INFO: {filepath} - no openGraph block (inherits from layout)')

# Fix tool detail page - add og:type if missing
print()
print('=== Fixing tool detail page OG tags ===')
with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if openGraph exists but missing type
if 'openGraph' in content and '"type":' not in content and "type:" not in content:
    # Add type after openGraph {
    content = content.replace(
        'openGraph: {',
        'openGraph: {\n      type: "product",'
    )
    print('Added og:type="product" to tool detail page')
else:
    print('Tool detail page already has og:type or no openGraph block')

with open('app/tools/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

# Fix category page - add og:type if missing
print()
print('=== Fixing category page OG tags ===')
with open('app/category/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

if 'openGraph' in content and '"type":' not in content and "type:" not in content:
    content = content.replace(
        'openGraph: {',
        'openGraph: {\n      type: "website",'
    )
    print('Added og:type="website" to category page')
else:
    print('Category page already has og:type or no openGraph block')

with open('app/category/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

# Fix alternatives page - add og:type if missing
print()
print('=== Fixing alternatives page OG tags ===')
with open('app/alternatives/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

if 'openGraph' in content and '"type":' not in content and "type:" not in content:
    content = content.replace(
        'openGraph: {',
        'openGraph: {\n      type: "article",'
    )
    print('Added og:type="article" to alternatives page')
else:
    print('Alternatives page already has og:type or no openGraph block')

with open('app/alternatives/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print()
print('=== OG tag fixes complete ===')
