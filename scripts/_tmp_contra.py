# -*- coding: utf-8 -*-
import io, sys, re, textwrap
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
fn = '2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md'
body = io.open(base + '\\' + fn, encoding='utf-8').read()
try:
    from llmevalkit.hallucination import ContradictionDetector
except Exception as e:
    print('import err:', e)
    raise SystemExit
det = ContradictionDetector()
# try common APIs
for method in ['detect', 'evaluate', 'check', 'score', 'predict']:
    if hasattr(det, method):
        print('has method:', method)
        try:
            r = getattr(det, method)(body)
            print('  ->', method, ':', str(r)[:800])
        except Exception as e:
            print('  -> err:', str(e)[:200])
