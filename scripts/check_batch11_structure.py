# -*- coding: utf-8 -*-
"""检查3篇重写草稿的结构指标：字数/H2/FAQ/内链/外链/截图"""
import re, os

FILES = [
    'content_drafts/2026-10-09-synthesia-vs-heygen_REWRITE.md',
    'content_drafts/2026-10-09-motion-ai-alternatives_REWRITE.md',
    'content_drafts/2026-10-09-quillbot-alternatives_REWRITE.md',
]

def wc(text):
    return len(text.split())

for f in FILES:
    text = open(f, encoding='utf-8').read()
    words = wc(text)
    h2 = re.findall(r'^##\s+.+', text, re.M)
    h3_faq = re.findall(r'^###\s+Q:', text, re.M)
    links = re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', text)
    internal = [u for t, u in links if '/blog/' in u or '/tools/' in u or '/compare/' in u]
    external = [u for t, u in links if u.startswith('http') and '/blog/' not in u and '/tools/' not in u and '/compare/' not in u and '/screenshots/' not in u]
    imgs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)
    has_quick = 'Quick Answer' in text
    print('=====', os.path.basename(f))
    print('  words:', words, '(need >2000)')
    print('  H2 count:', len(h2))
    for h in h2[:8]:
        print('    -', h)
    print('  FAQ Q count:', len(h3_faq), '(need >=3)')
    print('  internal links:', len(internal), internal[:6])
    print('  external links:', len(external), external[:5])
    print('  images:', len(imgs), imgs)
    print('  BLUF Quick Answer:', has_quick)
    print()
