# -*- coding: utf-8 -*-
import sys, inspect, io
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from llmevalkit.hallucination import ContradictionDetector
src = inspect.getsource(ContradictionDetector.evaluate)
print(src[1500:4000])
