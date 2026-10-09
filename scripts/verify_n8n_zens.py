# -*- coding: utf-8 -*-
"""n8n 草稿 zens-ink CLI 评分（与 batch12 verify 同口径：python -m zens_ink.content_qc <file>）"""
import json, re, os, subprocess, sys

BASE = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
DRAFT = os.path.join(BASE, 'content_drafts', '2026-10-09-n8n-review-2026_DRAFT.md')
tmp = os.path.join(BASE, 'window_logs', '_tmp_n8n_check.md')

with open(DRAFT, encoding='utf-8') as f:
    md = f.read()
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(md)

r = subprocess.run(['python', '-m', 'zens_ink.content_qc', tmp], capture_output=True, text=True, encoding='utf-8')
print(r.stdout)
print(r.stderr[:500] if r.stderr else '')
m = re.search(r'Score: (\d+)/100', r.stdout)
print('\n>> n8n zens-ink score:', m.group(1) if m else 'N/A')
os.remove(tmp)
