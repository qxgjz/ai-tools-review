import re
import os

files_to_check = [
    'app/page.tsx',
    'app/ranking/page.tsx',
    'app/category/[slug]/page.tsx',
    'app/tools/[slug]/page.tsx',
    'app/methodology/page.tsx',
    'app/about/page.tsx',
    'app/layout.tsx',
]

for filepath in files_to_check:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f'=== {filepath} ===')
        # 查找title
        title_matches = re.findall(r'title\s*[:=]\s*["\'](.*?)["\']', content)
        for t in title_matches[:3]:
            print(f'  Title: {t[:80]} ({len(t)} chars)')
        # 查找description
        desc_matches = re.findall(r'description\s*[:=]\s*["\'](.*?)["\']', content)
        for d in desc_matches[:3]:
            print(f'  Desc: {d[:80]} ({len(d)} chars)')
        print()
    else:
        print(f'=== {filepath} === NOT FOUND')
        print()
