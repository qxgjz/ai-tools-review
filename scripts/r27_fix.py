# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'
posts=json.load(io.open(fn,encoding='utf-8'))
MARK='<!-- r27-polish-20261022 -->'

def clean(s):
    s=re.sub(r'<[^>]+>','',s or '')
    s=re.sub(r'\s+',' ',s).strip()
    return s

# slug: (question_h2, [(label,url)...2], takeaway_bullets_or_None)
CFG={
'best-free-ai-tools-for-students-2026':(
 'Are the best free AI tools for students really free in 2026?',
 [('ChatGPT Free','https://chat.openai.com'),('Claude Free','https://claude.ai')],
 None),
'how-to-get-chatgpt-free-2026':(
 'How can I use ChatGPT for free in 2026 without a credit card?',
 [('ChatGPT Free tier','https://chat.openai.com'),('Microsoft Copilot','https://copilot.microsoft.com')],
 None),
'jasper-vs-copy-ai-2026-comparison':(
 'Jasper vs Copy.ai 2026: Which is better for marketing teams?',
 [('Jasper','https://www.jasper.ai'),('Copy.ai','https://www.copy.ai')],
 None),
'best-ai-chatbots-2026':(
 'Which AI chatbot should you choose in 2026?',
 [('ChatGPT','https://chat.openai.com'),('Claude','https://claude.ai')],
 None),
'best-ai-crm-tools-2026':(
 'What is the best AI CRM for teams in 2026?',
 [('HubSpot AI','https://www.hubspot.com'),('Salesforce Einstein GPT','https://www.salesforce.com')],
 None),
'best-ai-note-taking-tools-2026':(
 'Which AI note-taking tool avoids hallucination and keeps your data portable?',
 [('Notion AI','https://www.notion.so'),('Obsidian','https://obsidian.md')],
 None),
'best-ai-legal-tools-2026':(
 'What is the best AI legal tool for lawyers in 2026?',
 [('Harvey AI','https://www.harvey.ai'),('Clio','https://www.clio.com')],
 None),
'best-ai-seo-tools-2026':(
 'Which AI SEO tool gives the best ranking results in 2026?',
 [('Ahrefs','https://ahrefs.com'),('Semrush','https://www.semrush.com')],
 None),
'cursor-vs-github-copilot-2026-comparison':(
 'Cursor vs GitHub Copilot 2026: Which should developers choose?',
 [('Cursor','https://cursor.com'),('GitHub Copilot','https://github.com/features/copilot')],
 None),
}

changed=[]
by={p['slug']:p for p in posts}
for slug,(q,ext,kt) in CFG.items():
    p=by[slug]
    if MARK in p.get('content',''): continue
    qa=clean(p.get('quickAnswer',''))
    faqs=p.get('faq') or []
    # internal: reuse first 2 existing /blog/ links from body
    il=re.findall(r'\]\((/blog/[^)]+)\)',p['content'])[:2]
    lines=[MARK, '', f'**Bottom line:** {qa}', '']
    lines.append('**Official sources & related guides**')
    el=' | '.join(f'[{lbl}]({u})' for lbl,u in ext)
    lines.append(f'- {el}')
    if il:
        rel=' | '.join(f'[Related guide {i+1}]({u})' for i,u in enumerate(il))
        lines.append(f'- Related: {rel}')
    lines.append('')
    lines.append(f'## {q}')
    lines.append(qa or 'Compare the options on this page by pricing, ease of use, and fit for your workflow before choosing.')
    lines.append('')
    lines.append('## Frequently Asked Questions')
    lines.append('')
    for f in faqs[:3]:
        lines.append(f'### {clean(f.get("question",""))}')
        lines.append(clean(f.get('answer','')))
        lines.append('')
    block='\n'.join(lines).rstrip()+"\n\n"
    p['content']=block+p['content']
    changed.append(slug)

json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('changed',len(changed),changed)
