# -*- coding: utf-8 -*-
import io, os, sys, inspect, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, os.path.join(base, 'scripts'))
import llmevalkit.hallucination.core_detectors as cd
src = inspect.getsource(cd)
for name in ['_has_negation', '_sentence_similarity', '_split_sentences']:
    idx = src.find('def ' + name)
    print(src[idx:idx+1200])
    print('---')
