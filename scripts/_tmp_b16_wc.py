# -*- coding: utf-8 -*-
import io, os, sys, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, os.path.join(base, 'scripts'))
import llmevalkit.hallucination.core_detectors as cd
import zens_ink.content_qc as cq
# how zens_ink counts words
src = io.open(os.path.dirname(cq.__file__) + r'\content_qc.py', encoding='utf-8').read()
m = re.search(r'word_count[^\n]{0,120}', src)
print('word_count def area:')
for mm in re.finditer(r'def _[a-z_]+\(text[^)]*\)[^\n]*\n(?:[^\n]*\n){0,6}', src):
    print(mm.group(0)[:400])
    print('---')
