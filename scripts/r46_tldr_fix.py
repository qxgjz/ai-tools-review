# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
by={p['slug']:p for p in posts}
MARK='<!-- r46-tldr-20261102 -->'
def clean(s):
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s or ''); s=re.sub(r'<[^>]+>','',s); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
SLUGS=['notion-ai-vs-salesforce-2026','aider-review','best-ai-grammar-checker','best-ai-agents-2026',
'how-to-build-an-ai-agent','what-is-an-ai-agent','best-ai-voice-changers-content-creators',
'best-ai-coding-tools-beginners','best-ai-tools-for-beginners-2026','agenta-ai-review-2026',
'ai-video-generator-credits-burn-fast-2026','ai-tools-not-worth-the-money-2026']
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
