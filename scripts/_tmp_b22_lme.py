# -*- coding: utf-8 -*-
import io, re, sys
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from scripts.llmevalkit_toolkit import LMEvalKit
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
files = {
    'ai-video-generator-credits-burn-fast-2026': base + r'\content_drafts\2026-10-13-ai-video-generator-credits-burn-fast-2026_NEW.md',
    'ai-tools-not-worth-the-money-2026': base + r'\content_drafts\2026-10-13-ai-tools-not-worth-the-money-2026_NEW.md',
    'runway-vs-pika-2026': base + r'\content_drafts\2026-10-13-runway-vs-pika-2026_REWRITE.md',
}
for slug, path in files.items():
    md = io.open(path, encoding='utf-8').read()
    body = re.split(r'\n## Self-Check', md)[0]
    ev = LMEvalKit().evaluate_content(body, keyword=slug, context=body)
    print('=====', slug)
    print('score:', ev.get('score'), '| hallucination_detected:', ev.get('hallucination_detected'))
    ch = ev.get('checks', {}).get('hallucination', {})
    print('hallucination checks:', {k: v.get('score') for k, v in ch.items()})
