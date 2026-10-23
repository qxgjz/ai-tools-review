# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
gsc=['openai_astra_review','best-ai-voice-changers-2026','adobe-firefly-review-2026','ai-tools-for-beginners-2026','ai-coding-tools-comparison-2026','ai-tools-review-guide-2026','ai-tools-comparison-2026','best-ai-agents-2026-ranked-reviewed']
by={p['slug']:p for p in posts}
# supplement: long comparison/review listicles already having tool names
supp=['jasper-vs-copy-ai-2026-comparison','cursor-vs-github-copilot-2026-comparison','chatgpt-vs-gemini-2026-comparison','canva-ai-vs-adobe-firefly-2026-comparison','best-ai-chatbots-2026','best-ai-crm-tools-2026','best-ai-note-taking-tools-2026','best-ai-legal-tools-2026','best-ai-seo-tools-2026','best-ai-writing-tools-2026','midjourney-free-trial-2026','how-to-get-chatgpt-free-2026']
sel=gsc+[s for s in supp if s in by and s not in gsc]
print('selected',len(sel))
for s in sel:
    p=by[s]
    c=p['content']
    has_tbl=('|' in c and c.count('|')>=8)
    kt=[k for k in (p.get('keyTakeaways') or [])][:5]
    print(f"--- {s} | cat={p.get('category')} | table={has_tbl}")
    print('     KT=',json.dumps(kt,ensure_ascii=False)[:200])
