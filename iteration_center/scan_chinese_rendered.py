"""Scan all .tsx files for Chinese text in JSX (not comments)"""
import os
import re

results = []

for root, dirs, files in os.walk('.'):
    # Skip node_modules, .next, .git
    dirs[:] = [d for d in dirs if d not in ('node_modules', '.next', '.git', 'iteration_center')]
    for fname in files:
        if not fname.endswith(('.tsx', '.ts')):
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except:
            continue
        
        in_block_comment = False
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Track block comments
            if '/*' in stripped:
                in_block_comment = True
            if '*/' in stripped:
                in_block_comment = False
                continue
            if in_block_comment:
                continue
            if stripped.startswith('//'):
                continue
            
            # Look for Chinese characters
            if re.search(r'[\u4e00-\u9fff]', line):
                # Skip if it's in a string that's obviously a comment
                results.append(f"{fpath}:{i}: {stripped[:100]}")

print(f"Found {len(results)} lines with Chinese characters (non-comment):")
for r in results:
    print(f"  {r}")
