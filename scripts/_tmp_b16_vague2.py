# -*- coding: utf-8 -*-
import io, os, re, zens_ink
pkg = os.path.dirname(zens_ink.__file__)
# grep vague words usage
for root, dirs, files in os.walk(pkg):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            s = io.open(p, encoding='utf-8', errors='ignore').read()
            for m in re.finditer(r'vague', s, re.I):
                start = max(0, m.start()-100)
                seg = s[start:m.end()+200].replace('\n', ' ')
                if 'vague' in seg.lower():
                    print('FILE', f, '::', seg[:300])
                    print()
