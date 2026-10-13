# -*- coding: utf-8 -*-
import io
from llmevalkit.hallucination.core_detectors import ContradictionDetector
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
for slug in ['lovable-vs-boltnew', 'sudowrite-alternatives']:
    md = io.open(base + r'\content_drafts\2026-10-11-' + slug + '_REWRITE.md', encoding='utf-8').read()
    det = ContradictionDetector(use_llm=False)
    r = det.evaluate(answer=md, context=md)
    cons = r.details.get('contradictions', [])
    print('===', slug, '| count:', len(cons))
    for c in cons:
        print('  [', c['type'], '] ctx:', c['context_says'].replace('\n',' '))
        print('        out:', c['output_says'].replace('\n',' '))
