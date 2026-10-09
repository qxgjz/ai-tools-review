# -*- coding: utf-8 -*-
"""按 batch_zensink_final.py 相同逻辑验证 3 篇重写文章（确保最终入库分数 >=70）"""
import json
import re
import tempfile
from pathlib import Path
import sys
sys.path.insert(0, 'scripts')
from zens_ink import content_qc

with open('data/posts.json', encoding='utf-8') as f:
    posts = json.load(f)

slugs = ['midjourney-v7-vs-flux-2026', 'chatgpt-vs-claude-2026-comparison', 'claude-37-vs-gpt4o']
tmp_dir = tempfile.mkdtemp(prefix='zens_final_')
for p in posts:
    if p.get('slug') in slugs:
        title = p.get('title', '')[:60]
        content = p.get('content', '')
        text_content = re.sub(r'<[^>]+>', '', content)
        text_content = re.sub(r'&nbsp;', ' ', text_content)
        text_content = re.sub(r'&amp;', '&', text_content)
        tmp_file = Path(tmp_dir) / f"{p['slug'][:50]}.md"
        tmp_file.write_text(f"# {title}\n\n{text_content}", encoding='utf-8')
        r = content_qc.check_draft(tmp_file)
        print(f"=== {p['slug']}: score={r['score']} words={r['word_count']} fact={r['fact_density']} vague={r['vague_density']}")
        for c in r['checks']:
            if not c['pass']:
                print(f"   FAIL: {c['check']} ({c['note'][:80]})")
        print()
