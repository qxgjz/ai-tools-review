# -*- coding: utf-8 -*-
import io, sys
from llmevalkit.hallucination.core_detectors import ContradictionDetector
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
for slug in ['lovable-vs-boltnew', 'sudowrite-alternatives']:
    md = io.open(base + r'\content_drafts\2026-10-11-' + slug + '_REWRITE.md', encoding='utf-8').read()
    det = ContradictionDetector()
    res = det.detect(md)
    if isinstance(res, dict):
        issues = res.get('issues') or res.get('contradictions') or []
        print('===', slug, 'issues type:', type(issues).__name__)
        for it in issues[:8]:
            print('   ', str(it)[:200])
    else:
        print('===', slug, 'raw:', str(res)[:200])
