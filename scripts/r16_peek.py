import json, os, re
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in ['gemini-alternatives-2026','gemini-review-2026','github-copilot-review-2026']:
    p = next(x for x in posts if x['slug']==slug)
    c=p['content']
    print(f"=== {slug} ===")
    heads = re.findall(r'<h2[^>]*>(.*?)</h2>', c, flags=re.S|re.I)
    if not heads: heads = re.findall(r'^##\s+(.+)$', c, flags=re.M)
    for h in heads[:8]: print("  H2:", re.sub(r'<[^>]+>','',h)[:80])
    outb = re.findall(r'href="(https?://[^"]+)"', c)
    print("  outbound:", outb)
    print()
