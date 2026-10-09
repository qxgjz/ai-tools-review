# -*- coding: utf-8 -*-
"""复验入库版本的 zens-ink 评分：模拟 batch_zensink_final.py 逻辑
（剥HTML + markdown分支判定），确认 posts.json 中的 content 达标。
同时核对 git diff 范围。
"""
import json
import re
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

with open('data/posts.json', encoding='utf-8') as f:
    posts = json.load(f)

def strip_html(html: str) -> str:
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html).strip()

for slug in ['synthesia-vs-heygen', 'motion-ai-alternatives', 'quillbot-alternatives']:
    p = next(x for x in posts if x.get('slug') == slug)
    c = p['content']
    # 写入临时md文件（按batch逻辑：HTML则剥标签；markdown直接评分）
    tmp = 'window_logs/_tmp_check.md'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(c)
    r = subprocess.run(['python', '-m', 'zens_ink.content_qc', tmp], capture_output=True, text=True, encoding='utf-8')
    out = r.stdout
    m = re.search(r'Score: (\d+)/100', out)
    print(slug, '| score:', m.group(1) if m else 'N/A')
    # 提取各检查项
    for line in out.splitlines():
        if '[PASS]' in line or '[FIX ]' in line or '[WARN]' in line:
            print('   ', line.strip()[:90])

os.remove('window_logs/_tmp_check.md')

# git diff 统计
print('\n=== git diff --stat ===')
r = subprocess.run(['git', 'diff', '--stat'], capture_output=True, text=True)
print(r.stdout)
