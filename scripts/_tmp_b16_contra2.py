# -*- coding: utf-8 -*-
import io, os, sys, inspect
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, os.path.join(base, 'scripts'))
from llmevalkit_toolkit import LMEvalKit
ev = LMEvalKit()
hall = ev._modules['hallucination']
import llmevalkit
print('llmevalkit pkg:', os.path.dirname(llmevalkit.__file__))
# find ContradictionDetector source
import llmevalkit.hallucination as hmod
src = inspect.getsource(hmod)
print('has ContradictionDetector:', 'ContradictionDetector' in src)
# print the class
idx = src.find('class ContradictionDetector')
print(src[idx:idx+3000])
