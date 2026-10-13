# -*- coding: utf-8 -*-
import io, json, subprocess, sys, time
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
# only scan content-type articles that are NOT already rewritten (wordCount >= 2000 or content is markdown)
results = []
for p in posts:
    slug = p.get('slug', '')
    content = p.get('content', '')
    if not content:
        continue
    wc = p.get('wordCount', 0)
    if wc >= 2000:
        continue  # already rewritten to standard
    tmp = base + r'\scripts\_tmp_b20_scan_' + slug.replace('/', '_') + '.md'
    io.open(tmp, 'w', encoding='utf-8').write(content[:30000])
    out = subprocess.run([sys.executable, '-m', 'zens_ink.content_qc', tmp, '--format', 'json'],
                         capture_output=True, text=True, encoding='utf-8')
    try:
        res = json.loads(out.stdout)
        score = res[0]['score'] if isinstance(res, list) else res.get('score')
    except Exception:
        score = -1
    results.append((slug, score, wc))
    print(slug, score)
for slug, score, wc in sorted(results, key=lambda x: x[1]):
    if score < 70:
        print('LOW:', slug, score, 'wc', wc)
