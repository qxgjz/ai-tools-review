# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
by={p['slug']:p for p in posts}
MARK='<!-- r43-tldr-20261101 -->'
def clean(s):
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s or ''); s=re.sub(r'<[^>]+>','',s); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
SLUGS=['best-ai-project-management-tools-2026','best-ai-transcription-tools-2026','dify_ai_review',
'cursor_ai_review','gemini_38_flash_review','elevenlabs-review-2026','suno-review-2026',
'surfer-seo-vs-frase-2026-comparison','gemini-vs-chatgpt-2026','otter-ai-alternatives',
'autochain-review-2026','chatgpt-alternatives-2026']
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
