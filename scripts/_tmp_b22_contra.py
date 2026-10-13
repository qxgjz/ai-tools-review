# -*- coding: utf-8 -*-
import io, re, sys, json
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from llmevalkit.hallucination.core_detectors import ContradictionDetector
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
p1 = base + r'\content_drafts\2026-10-13-ai-video-generator-credits-burn-fast-2026_NEW.md'
md = io.open(p1, encoding='utf-8').read()
body = re.split(r'\n## Self-Check', md)[0]
det = ContradictionDetector(use_llm=False)
res = det.evaluate(answer=body, context=body)
d = res.model_dump()
print(json.dumps(d['details'], ensure_ascii=False, indent=1)[:4000])
