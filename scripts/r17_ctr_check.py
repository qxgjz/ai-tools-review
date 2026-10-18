import json, os, re
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in ['adobe-firefly-review-2026','ai-tools-comparison-2026','best-ai-voice-changers-2026','creatium-coach-review-2025','elevenlabs-review-2026']:
    p=next((x for x in posts if x['slug']==slug),None)
    if not p: print(slug,'NOT IN posts'); continue
    t=p.get('title',''); e=p.get('excerpt','')
    print(f"{slug}\n  TITLE {len(t)}c: {t}\n  EXCERPT {len(e)}c: {e}\n")
# redirects
red=open('public/_redirects','r',encoding='utf-8').read().splitlines()
for ln in red:
    if 'article-api' in ln and ('creatium' in ln or 'elevenlabs' in ln):
        print('REDIR:',ln)
