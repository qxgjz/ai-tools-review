# -*- coding: utf-8 -*-
import sys, inspect
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from llmevalkit.hallucination import ContradictionDetector
print('signature:', inspect.signature(ContradictionDetector.evaluate))
print(inspect.getsource(ContradictionDetector.evaluate)[:1500])
