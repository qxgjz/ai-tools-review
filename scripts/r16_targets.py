import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
slugs = {p['slug'] for p in posts}
for t in ['creatium-coach-review-2025','elevenlabs-review-2026','best-ai-voice-changers-2026']:
    print(t, 'EXISTS' if t in slugs else 'MISSING')
p = next(x for x in posts if x['slug']=='best-ai-voice-changers-2026')
print('\nVOICE-CHANGERS full:')
print('TITLE:', repr(p['title']), len(p['title']),'c')
print('EXCERPT:', repr(p.get('excerpt')), len(p.get('excerpt','')),'c')
# any article-api posts still present?
api = [x['slug'] for x in posts if 'article-api' in x['slug']]
print('\narticle-api posts still in data:', api)
