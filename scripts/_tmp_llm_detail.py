# -*- coding: utf-8 -*-
import io, sys, json
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
files = [('2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md', 'best ai tools for beginners 2026'),
         ('2026-10-10-agenta-ai-review-2026_DRAFT.md', 'agenta ai review open source agent builder')]
from scripts.llmevalkit_toolkit import LMEvalKit
ev = LMEvalKit()
for fn, kw in files:
    body = io.open(base + '\\' + fn, encoding='utf-8').read()
    res = ev.evaluate_content(body, keyword=kw, context=body)
    print('===', fn)
    print(json.dumps(res, ensure_ascii=False, indent=1)[:4000])
    print()
