import json, os, re
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
p = next(x for x in posts if x['slug']=='cursor-vs-github-copilot-2026')
c = p['content']
print("=== HEAD 700 ===")
print(c[:700])
print("\n=== outbound http links ===")
for m in re.findall(r'\((https?://[^)]+)\)', c):
    print(" ", m)
print("\n=== FAQ present?", 'FAQ' in c or 'frequently' in c.lower())
print("\n=== TAIL 900 ===")
print(c[-900:])
