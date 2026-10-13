# -*- coding: utf-8 -*-
import io, sys, importlib, inspect
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from llmevalkit.hallucination import ContradictionDetector
mod = importlib.import_module(ContradictionDetector.__module__)
print('NEGATION_WORDS:', mod.NEGATION_WORDS)
_split = mod._split_sentences
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
body = io.open(base + r'\2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md', encoding='utf-8').read()
sents = _split(body)
s = sents[38]
print('sent38 full:')
print(s[:600])
w = set(s.lower().split())
print('neg words hit:', w & mod.NEGATION_WORDS)
