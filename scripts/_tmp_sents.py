# -*- coding: utf-8 -*-
import io, sys, importlib, inspect
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from llmevalkit.hallucination import ContradictionDetector
mod = importlib.import_module(ContradictionDetector.__module__)
_split = mod._split_sentences
_sim = mod._sentence_similarity
_neg = mod._has_negation
print('has_negation source:')
print(inspect.getsource(_neg))
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
body = io.open(base + r'\2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md', encoding='utf-8').read()
sents = _split(body)
print('num sentences:', len(sents))
# print sentences containing '## ' or '|' with negation status and short content
for i, s in enumerate(sents):
    t = s.strip()
    if '## ' in t or '|' in t or 'no need' in t or 'costs nothing' in t:
        print(i, 'neg=', _neg(s), '|', t[:110])
