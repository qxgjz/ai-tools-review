# -*- coding: utf-8 -*-
"""把3篇草稿的完整URL内链改为相对路径（zens_ink markdown内链判定要求](/path)）
图片链接也改为相对路径（与上轮入库文章一致）
"""
import re

FILES = [
    'content_drafts/2026-10-09-synthesia-vs-heygen_REWRITE.md',
    'content_drafts/2026-10-09-motion-ai-alternatives_REWRITE.md',
    'content_drafts/2026-10-09-quillbot-alternatives_REWRITE.md',
]

for f in FILES:
    text = open(f, encoding='utf-8').read()
    # 内链: https://aitoolcrux.com/blog/xxx -> /blog/xxx
    new = re.sub(r'\]\(https://aitoolcrux\.com(/blog/[^)]+)\)', r'](\1)', text)
    # 图片: https://aitoolcrux.com/screenshots/... -> /screenshots/...
    new = re.sub(r'!\[([^\]]*)\]\(https://aitoolcrux\.com(/screenshots/[^)]+)\)', r'![\1](\2)', new)
    changed = sum(1 for a, b in zip(text.split('\n'), new.split('\n')) if a != b)
    open(f, 'w', encoding='utf-8').write(new)
    rel = re.findall(r'\]\((/blog/[^)]+)\)', new)
    ext = re.findall(r'\]\((https?://[^)]+)\)', new)
    imgs = re.findall(r'!\[[^\]]*\]\((/[^)]+)\)', new)
    print(f)
    print('  changed lines:', changed, '| relative internal:', len(rel), rel[:5])
    print('  external:', len(ext), '| images(relative):', len(imgs))
