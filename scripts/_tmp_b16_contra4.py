# -*- coding: utf-8 -*-
import io, os, sys, inspect, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, os.path.join(base, 'scripts'))
import llmevalkit.hallucination as hmod
src = inspect.getsource(hmod)
# list class names
for m in re.finditer(r'class\s+(\w+)', src):
    print(m.group(1))
