# -*- coding: utf-8 -*-
"""检查 batch12 三篇草稿的结构指标"""
import re

FILES = [
    'content_drafts/2026-10-09-runway-alternatives_REWRITE.md',
    'content_drafts/2026-10-09-writesonic-alternatives_REWRITE.md',
    'content_drafts/2026-10-09-otter-ai-alternatives_REWRITE.md',
]

for f in FILES:
    try:
        text = open(f, encoding='utf-8').read()
    except FileNotFoundError:
        print('SKIP', f)
        continue
    body = text.split('\n---\n\n## Self-Check Report')[0]
    words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", body))
    h2 = re.findall(r'^## (.+)$', body, re.M)
    faq = len(re.findall(r'^### Q:', body, re.M))
    rel = re.findall(r'\]\((/blog/[^)]+)\)', body)
    ext = re.findall(r'\]\((https?://[^)]+)\)', body)
    imgs = re.findall(r'!\[[^\]]*\]\((/[^)]+)\)', body)
    qh = [h for h in h2 if '?' in h]
    print('=====', f)
    print('  words:', words, '(need >2000) | H2:', len(h2), '| FAQ:', faq)
    print('  internal:', len(rel), rel)
    print('  external:', len(ext), ext)
    print('  images:', len(imgs), imgs)
    print('  BLUF:', 'Bottom line' in body[:3000], '| question H2:', len(qh), qh[:3])
