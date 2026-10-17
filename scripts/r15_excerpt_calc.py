import json, os, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc
posts = json.load(open('data/posts.json','r',encoding='utf-8'))

cands = [
 "Cursor vs GitHub Copilot 2026: which AI coding tool wins? We tested both 30 days — pricing, accuracy, and verdict for solo devs and teams.",
 "Cursor vs GitHub Copilot 2026: which AI coding tool wins? Real 30-day test: pricing, accuracy, IDE support, and our verdict for devs and teams.",
 "Cursor vs GitHub Copilot 2026: which wins? We tested both 30 days on real projects — pricing, accuracy, IDE support, and verdict for devs.",
]
for c in cands:
    print(len(c), "OK" if 120<=len(c)<=155 else "XX", c)
