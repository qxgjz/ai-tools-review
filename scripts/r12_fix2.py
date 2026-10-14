import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
p = next(x for x in posts if x['slug']=='best-free-ai-tools-for-youtube-creators')
p['excerpt'] = 'Best free AI tools for YouTube creators in 2026: CapCut editing, ElevenLabs voiceover, ChatGPT scripts, Canva thumbnails. No credit card needed.'
print('excerpt len:', len(p['excerpt']))
json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
