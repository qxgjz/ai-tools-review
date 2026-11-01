# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
by={p['slug']:p for p in posts}
MARK='<!-- r44-tldr-20261101 -->'
def clean(s):
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s or ''); s=re.sub(r'<[^>]+>','',s); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
SLUGS=['runway-vs-pika-2026','best-free-ai-tools-for-students-2026','cursor-vs-github-copilot-2026',
'elevenlabs-vs-playht-2026','canva-pro-free-for-students','midjourney-v7-vs-dall-e-3-ecommerce',
'claude-alternatives-2026','notion-ai-vs-obsidian-ai','lovable-vs-boltnew','claude-37-vs-gpt4o',
'synthesia-vs-heygen','beautiful-ai-alternatives']
done=[]
for sl in SLUGS:
    p=by.get(sl)
    if not p or '## TL;DR' in p['content']: continue
    qa=clean(p.get('quickAnswer','')).replace('Quick Answer:','').strip()
    if len(qa)<45 or qa.lower().startswith(('quick answer','http')):
        title=clean(p.get('title',''))
        qa=f'{title}. Compare pricing, ease of use and output quality before choosing a tool for your workflow.'
    kt=[clean(x) for x in (p.get('keyTakeaways') or []) if clean(x)]
    block=[MARK,'','## TL;DR','',qa,'']
    if kt:
        block+=['**Key takeaways:**','']
        for k in kt[:5]: block.append(f'- {k}')
        block.append('')
    p['content']='\n'.join(block).rstrip()+"\n\n"+p['content']
    done.append(sl)
json.dump(posts,io.open('data/posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('done',len(done),done)
