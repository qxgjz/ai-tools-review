# -*- coding: utf-8 -*-
import io, os, sys, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, os.path.join(base, 'scripts'))
from llmevalkit_toolkit import LMEvalKit
import inspect
print(inspect.signature(LMEvalKit.evaluate_content))
ev = LMEvalKit()
p = os.path.join(base, 'content_drafts', '2026-10-11-gemini-vs-chatgpt-2026_REWRITE.md')
body = io.open(p, encoding='utf-8').read()
r = ev.evaluate_content(body, keyword='gemini vs chatgpt', context=body)
print(json.dumps(r, ensure_ascii=False, indent=1, default=str)[:6000])
