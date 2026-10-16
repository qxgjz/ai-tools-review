import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
fixes = {
    'canva-ai-alternatives-2026': 'Best Canva AI alternatives in 2026: Adobe Express, Figma, VistaCreate. We tested pricing, AI features, and pros/cons to help you switch.',
    'chatgpt-alternatives-2026': 'Best ChatGPT alternatives in 2026: Claude 3.5, Gemini Advanced, Perplexity Pro. We tested each for writing, search, and multimodal tasks.',
}
for slug, exc in fixes.items():
    p = next(x for x in posts if x['slug']==slug)
    p['excerpt'] = exc
    print(f"{slug}: {len(exc)}c")
json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
