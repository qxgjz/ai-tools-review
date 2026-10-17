import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

def html_to_md(html):
    s = html
    s = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', s, flags=re.S|re.I)
    s = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', s, flags=re.S|re.I)
    s = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', s, flags=re.S|re.I)
    s = re.sub(r'<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>', r'**\1**', s, flags=re.S|re.I)
    s = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', s, flags=re.S|re.I)
    s = re.sub(r'</?[uo]l[^>]*>', '', s, flags=re.I)
    s = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', s, flags=re.S|re.I)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

posts = json.load(open('data/posts.json','r',encoding='utf-8'))

def prep(slug):
    p = next(x for x in posts if x['slug']==slug)
    c = p['content']
    if '<' in c[:300]:
        c = html_to_md(c)
    return p, c

# 1) gemini-alternatives: BLUF + question H2 + 1 outbound
p, c = prep('gemini-alternatives-2026')
if 'Bottom line' not in c:
    bluf = ("**Bottom line:** For most users leaving Gemini, ChatGPT remains the strongest all-round alternative, "
            "Claude wins long-document reasoning, and Perplexity is best for cited web research.\n\n")
    c = bluf + c
if 'What Is the Best Gemini Alternative' not in c:
    q = ("## What Is the Best Gemini Alternative in 2026?\n\n"
         "ChatGPT is the best overall Gemini alternative in 2026; choose Claude for long writing and Perplexity for "
         "up-to-date sourced answers.\n\n")
    c = c.replace('## Quick Answer', q + '## Quick Answer', 1)
if len(re.findall(r'\]\(https?://[^)]+\)', c)) < 2:
    c += "\n\n- [Claude by Anthropic](https://www.anthropic.com/claude)\n"
p['content'] = c

# 2) gemini-review: BLUF + 1 outbound
p, c = prep('gemini-review-2026')
if 'Bottom line' not in c:
    bluf = ("**Bottom line:** Google Gemini (free tier) is the best general-purpose model for search-grounded answers "
            "and Gmail/Docs integration, though Claude edges it on long-form reasoning.\n\n")
    c = bluf + c
if len(re.findall(r'\]\(https?://[^)]+\)', c)) < 2:
    c += "\n\n- [Google Gemini official](https://gemini.google.com/)\n"
p['content'] = c

# 3) github-copilot-review: BLUF only
p, c = prep('github-copilot-review-2026')
if 'Bottom line' not in c:
    bluf = ("**Bottom line:** GitHub Copilot is the default AI pair programmer for teams already on GitHub: cheap, "
            "IDE-agnostic, and strongest with native code-review integration.\n\n")
    c = bluf + c
p['content'] = c

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

# verify
for slug in ['gemini-alternatives-2026','gemini-review-2026','github-copilot-review-2026']:
    p = next(x for x in posts if x['slug']==slug)
    exc = p.get('excerpt','')[:160]
    md = f"---\ntitle: \"{p['title']}\"\ndescription: \"{exc}\"\ndate: 2026-10-17\n---\n\n{p['content']}\n"
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.md'
    tmp.write_text(md, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    fails = [ch['check'] for ch in r['checks'] if not ch['pass']]
    print(f"{slug}: {r['score']} fails={fails}")
