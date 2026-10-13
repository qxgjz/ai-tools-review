# -*- coding: utf-8 -*-
import io, json, re, subprocess, sys, os
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
targets = ['devin-ai-review', 'claude-opus-4-vs-gpt-5-2026', 'perplexity-vs-chatgpt-2026']
tmpdir = base + r'\scripts\_tmp_b21_md'
os.makedirs(tmpdir, exist_ok=True)
for slug in targets:
    p = next((x for x in posts if x.get('slug') == slug), None)
    if p is None:
        print(slug, 'NOT FOUND'); continue
    content = p.get('content', '')
    md = re.sub(r'<[^>]+>', ' ', content)
    md = re.sub(r'\s+', ' ', md)[:30000]
    tmp = tmpdir + '\\' + slug + '.md'
    io.open(tmp, 'w', encoding='utf-8').write(md)
    out = subprocess.run([sys.executable, '-m', 'zens_ink.content_qc', tmp, '--format', 'json'], capture_output=True, text=True, encoding='utf-8')
    try:
        res = json.loads(out.stdout)
        score = res[0]['score'] if isinstance(res, list) else res.get('score')
    except Exception:
        score = 'ERR'
    print(slug, '| wordCount:', p.get('wordCount'), '| zens-ink:', score)
