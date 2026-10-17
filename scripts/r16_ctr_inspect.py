import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
by = {p['slug']:p for p in posts}
slugs = {
 'adobe-firefly-review-2026':'CTR-01',
 'ai-tools-comparison-2026':'CTR-02',
 'best-ai-voice-changers-2026':'CTR-06',
}
for slug,tag in slugs.items():
    p = by.get(slug)
    if not p:
        print(f"{tag} {slug}: NOT IN POSTS"); continue
    t=p.get('title',''); ex=p.get('excerpt','')
    print(f"=== {tag} {slug} ===")
    print(f"  title {len(t)}c: {t}")
    print(f"  excerpt {len(ex)}c: {ex}")
    bluf = 'Bottom line' in p.get('content','')
    outb = p.get('content','').count('](http') + p.get('content','').count('](https')
    print(f"  BLUF={bluf} outbound={outb}")
    print()
# R15 survivors
for slug in ['cursor-vs-github-copilot-2026','dall-e-3-review-2026','figma-ai-review-2026']:
    p=by.get(slug)
    if p:
        print(f"R15 survivor {slug}: BLUF={'Bottom line' in p.get('content','')} excerpt {len(p.get('excerpt',''))}c")
