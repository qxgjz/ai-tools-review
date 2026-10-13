# -*- coding: utf-8 -*-
import io
from llmevalkit.hallucination import core_detectors as cd
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
for slug in ['lovable-vs-boltnew', 'sudowrite-alternatives']:
    md = io.open(base + r'\content_drafts\2026-10-11-' + slug + '_REWRITE.md', encoding='utf-8').read()
    det = cd.ContradictionDetector(use_llm=False)
    r = det.evaluate(answer=md, context=md)
    print('===', slug, '| score:', r.score)
    print('  reason:', (r.reason or '')[:300])
