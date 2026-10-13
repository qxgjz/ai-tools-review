# -*- coding: utf-8 -*-
import io, os, re
import zens_ink
pkg_dir = os.path.dirname(zens_ink.__file__)
print('pkg dir:', pkg_dir)
for root, dirs, files in os.walk(pkg_dir):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            s = io.open(p, encoding='utf-8', errors='ignore').read()
            if 'vague' in s.lower():
                m = re.search(r'(VAGUE|vague)[^=]*?=\s*\[[^\]]{0,3000}\]', s)
                if m:
                    print('---', f)
                    print(m.group(0)[:3000])
                    print()
