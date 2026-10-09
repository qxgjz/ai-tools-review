# -*- coding: utf-8 -*-
"""复验 batch12 入库版本 zens-ink 评分（剥HTML+markdown分支），并查 diff 范围"""
import json
import re
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

with open('data/posts.json', encoding='utf-8') as f:
    posts = json.load(f)

for slug in ['runway-alternatives', 'writesonic-alternatives', 'otter-ai-alternatives']:
    p = next(x for x in posts if x.get('slug') == slug)
    tmp = 'window_logs/_tmp_check12.md'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(p['content'])
    r = subprocess.run(['python', '-m', 'zens_ink.content_qc', tmp], capture_output=True, text=True, encoding='utf-8')
    m = re.search(r'Score: (\d+)/100', r.stdout)
    print(slug, '| score:', m.group(1) if m else 'N/A', '| wc:', p.get('wordCount'), '| imgs:', p.get('screenshotCount'))
    for line in r.stdout.splitlines():
        if '[FIX ]' in line:
            print('   ', line.strip()[:80])
os.remove('window_logs/_tmp_check12.md')

print('\n=== git diff --stat (data/iteration_center only) ===')
r = subprocess.run(['git', 'diff', '--stat', 'data/posts.json', 'iteration_center/state.json'], capture_output=True, text=True)
print(r.stdout)
