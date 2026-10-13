# -*- coding: utf-8 -*-
import io, os, sys
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, os.path.join(base, 'scripts'))
import llmevalkit.hallucination.core_detectors as cd
for slug in ['gemini-vs-chatgpt-2026', 'elevenlabs-v2-review-2026']:
    p = os.path.join(base, 'content_drafts', '2026-10-11-%s_REWRITE.md' % slug)
    body = io.open(p, encoding='utf-8').read()
    d = cd.ContradictionDetector(use_llm=False)
    r = d.evaluate(answer=body, context=body)
    print('===', slug, '| score:', r.score)
    det = getattr(r, 'details', {})
    a_sents = cd._split_sentences(body)
    for c in det.get('contradictions', []):
        ctx = c['context_says']; out = c['output_says']
        # find full sentences in body
        full_ctx = next((s for s in a_sents if s.startswith(ctx)), ctx)
        full_out = next((s for s in a_sents if s.startswith(out)), out)
        print('  CTX full:', full_ctx[:220])
        print('     neg:', cd._has_negation(full_ctx))
        print('  OUT full:', full_out[:220])
        print('     neg:', cd._has_negation(full_out))
        print()
