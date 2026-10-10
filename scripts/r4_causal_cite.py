import json, os, re
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))

# 给两篇补权威来源链接
ADD_LINKS = {
    'claude-37-vs-gpt4o': '''
<h3>Sources</h3>
<ul>
<li>Anthropic. <a href="https://www.anthropic.com/news/claude-3-7-sonnet">Introducing Claude 3.7 Sonnet</a> — official release notes (Feb 2025).</li>
<li>Anthropic. <a href="https://www.anthropic.com/pricing">Claude API Pricing</a> — $3/M input, $15/M output.</li>
<li>OpenAI. <a href="https://openai.com/api/pricing/">GPT-4o API Pricing</a> — $2.50/M input, $10/M output.</li>
<li>SWE-bench. <a href="https://www.swebench.com/">Verified leaderboard</a> — Claude 3.7 extended thinking scores 62%.</li>
</ul>
''',
    'midjourney-v7-vs-flux-2026': '''
<h3>Sources</h3>
<ul>
<li>Black Forest Labs. <a href="https://docs.bfl.ai/flux_1_1_pro/">FLUX1.1 [pro] Documentation</a> — $0.04 per image API pricing.</li>
<li>Midjourney. <a href="https://docs.midjourney.com/plans">Pricing Plans</a> — $10/$30/$60 per month tiers.</li>
<li>Anthropic. <a href="https://www.anthropic.com/news/claude-3-7-sonnet">Claude 3.7 Sonnet announcement</a>.</li>
</ul>
''',
}

for slug, extra in ADD_LINKS.items():
    p = next((x for x in posts if x['slug']==slug), None)
    if not p:
        print(f'{slug}: NOT FOUND, skip'); continue
    if '<h3>Sources</h3>' in p['content']:
        print(f'{slug}: sources already added, skip'); continue
    # Insert before FAQ
    if '<h2>Frequently Asked Questions</h2>' in p['content']:
        p['content'] = p['content'].replace('<h2>Frequently Asked Questions</h2>',
                                              extra + '\n<h2>Frequently Asked Questions</h2>', 1)
    else:
        p['content'] = p['content'] + '\n' + extra
    print(f'{slug}: sources appended')

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
