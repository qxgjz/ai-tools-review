# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8'))
MARK='<!-- r29-low-20261023 -->'
def clean(s):
    s=re.sub(r'<[^>]+>','',s or ''); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
CFG={
'cursor-alternatives-2026':('What is the best free Cursor alternative in 2026?',[('GitHub Copilot','https://github.com/features/copilot'),('Claude Code','https://www.anthropic.com/claude-code')],['/blog/cursor-vs-github-copilot-2026-comparison','/blog/best-ai-coding-tools-2026']),
'free-ai-tools-for-students-2026':('Which free AI tools are genuinely free for students in 2026?',[('Grammarly','https://www.grammarly.com'),('Google Gemini for Education','https://edu.google.com')],None),
'perplexity-alternatives-2026':('What is the best Perplexity alternative in 2026?',[('Perplexity','https://www.perplexity.ai'),('You.com','https://you.com')],None),
'best-ai-mental-health-apps-2026':('Which AI mental health app should you choose in 2026?',[('Headspace','https://www.headspace.com'),('Wysa','https://www.wysa.io')],None),
'best-ai-meeting-notes-tools-2026':('What is the best AI meeting notes tool in 2026?',[('Fireflies.ai','https://fireflies.ai'),('Otter.ai','https://otter.ai')],None),
'n8n-vs-zapier-2026':('n8n vs Zapier 2026: Which automation tool wins?',[('Zapier','https://zapier.com'),('n8n','https://n8n.io')],None),
}
by={p['slug']:p for p in posts}; changed=[]
for slug,(q,ext,ilov) in CFG.items():
    p=by[slug]
    if MARK in p['content']: continue
    qa=clean(p.get('quickAnswer',''))
    kt=[clean(x) for x in (p.get('keyTakeaways') or []) if clean(x)]
    faqs=p.get('faq') or []
    il=re.findall(r'\]\((/blog/[^)]+)\)',p['content'])[:2]
    il=il or (ilov or [])
    lines=[MARK,'',f'**Bottom line:** {qa}','','**Official sources**']
    lines+= [f'- [{l}]({u})' for l,u in ext]
    if il:
        lines.append('**Related guides**')
        lines+=[f'- [Related guide {i+1}]({u})' for i,u in enumerate(il)]
    if kt:
        lines+=['','**Key takeaways**']
        lines+=[f'- {k}' for k in kt[:5]]
    lines+=['',f'## {q}',qa or 'Compare the options on this page by pricing, ease of use, and fit for your workflow.','','## Frequently Asked Questions','']
    for f in faqs[:3]:
        lines.append(f'### {clean(f.get("question",""))}'); lines.append(clean(f.get('answer',''))); lines.append('')
    block='\n'.join(lines).rstrip()+"\n\n"
    p['content']=block+p['content']; changed.append(slug)
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('changed',len(changed),changed)
