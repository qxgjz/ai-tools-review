# -*- coding: utf-8 -*-
import io, os, sys, re, glob
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, os.path.join(base, 'scripts'))
import llmevalkit
pkg = os.path.dirname(llmevalkit.__file__)
print('pkg:', pkg)
for p in glob.glob(pkg + r'\**\*.py', recursive=True):
    s = io.open(p, encoding='utf-8', errors='ignore').read()
    cls = re.findall(r'class\s+(\w+)', s)
    if any('Contradiction' in c or 'contradiction' in s for c in cls) or 'negation_flip' in s:
        print('FILE:', os.path.relpath(p, pkg), '| classes:', [c for c in cls if 'ontra' in c or 'egation' in c])
        for m in re.finditer(r'negation_flip', s):
            seg = s[max(0,m.start()-400):m.end()+200]
            print('  ...', seg[:700].replace('\n',' | '))
            print()
