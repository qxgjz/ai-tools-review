# -*- coding: utf-8 -*-
import io, sys, re
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
from llmevalkit.hallucination.contradiction import _split_sentences, _sentence_similarity, _has_negation

def find(fn):
    body = io.open(base + '\\' + fn, encoding='utf-8').read()
    a_sents = _split_sentences(body)
    c_sents = _split_sentences(body)
    pairs = []
    for a in a_sents:
        for c in c_sents:
            if a == c:
                continue
            sim = _sentence_similarity(a, c)
            if sim < 0.3:
                continue
            al, cl = a.lower(), c.lower()
            # antonym
            antonyms = {'approved':'rejected','accepted':'denied','increase':'decrease','profit':'loss','success':'failure','safe':'dangerous','true':'false','correct':'incorrect','valid':'invalid','active':'inactive','positive':'negative','present':'absent','include':'exclude','allow':'prohibit','compliant':'non-compliant'}
            antonyms.update({v:k for k,v in antonyms.items()})
            hit = None
            for w, op in antonyms.items():
                if w in al and op in cl:
                    hit = ('antonym', w, op)
                    break
            if hit:
                pairs.append((sim, hit[0], a[:90], c[:90]))
            elif _has_negation(a) != _has_negation(c) and sim > 0.5:
                pairs.append((sim, 'negation_flip', a[:90], c[:90]))
    seen = set()
    out = []
    for sim, typ, a, c in pairs:
        key = (a, c)
        if key in seen:
            continue
        seen.add(key)
        out.append((sim, typ, a, c))
    print('===', fn, '| pairs:', len(out))
    for sim, typ, a, c in sorted(out, reverse=True)[:25]:
        print('  [%.2f %s] A: %s ||| C: %s' % (sim, typ, a, c))
    print()

find('2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md')
find('2026-10-10-agenta-ai-review-2026_DRAFT.md')
