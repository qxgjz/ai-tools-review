# -*- coding: utf-8 -*-
import io, json, re, sys, subprocess
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from llmevalkit.hallucination.core_detectors import ContradictionDetector
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
PY = r'C:\Users\通明街\AppData\Local\DoubaoWork\User Data\sandbox_runtime\bases\d0ace100fdff5b2d247847aca1e3d83b\python\python.exe'

def words_of(t):
    return len(re.findall(r"[A-Za-z][A-Za-z'-]*", t))

def zens(path):
    out = subprocess.run([PY, '-m', 'zens_ink.content_qc', path, '--format', 'json'],
                         capture_output=True, text=True, encoding='utf-8')
    try:
        data = json.loads(out.stdout)
        return data[0]['score'] if isinstance(data, list) else data.get('score', 0)
    except Exception:
        return 'ERR:' + out.stdout[-100:]

files = {
    'ai-video-generator-credits-burn-fast-2026': base + r'\content_drafts\2026-10-13-ai-video-generator-credits-burn-fast-2026_NEW.md',
    'ai-tools-not-worth-the-money-2026': base + r'\content_drafts\2026-10-13-ai-tools-not-worth-the-money-2026_NEW.md',
    'runway-vs-pika-2026': base + r'\content_drafts\2026-10-13-runway-vs-pika-2026_REWRITE.md',
}
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
slugs = set(p.get('slug') for p in posts) | {'ai-video-generator-credits-burn-fast-2026', 'ai-tools-not-worth-the-money-2026'}

for slug, path in files.items():
    md = io.open(path, encoding='utf-8').read()
    body = re.split(r'\n## Self-Check', md)[0]
    w = words_of(body)
    h2 = re.findall(r'^## (.+)$', body, re.M)
    faq = len(re.findall(r'^### ', body, re.M))
    imgs = re.findall(r'!\[[^\]]*\]\((/screenshots/[^)]+)\)', body)
    internal = re.findall(r'\]\(/blog/([^)]+)/\)', body)
    external = re.findall(r'\]\((https?://[^)]+)\)', body)
    internal_ok = [s for s in internal if s in slugs]
    # zens-ink
    zs = zens(path)
    # llmevalkit contradiction
    det = ContradictionDetector(use_llm=False)
    cr = det.evaluate(answer=body, context=body).model_dump()
    cons = cr['details'].get('contradictions', [])
    print('=====', slug)
    print('words:', w, '| H2:', len(h2), '| FAQ:', faq, '| imgs:', len(imgs), imgs)
    print('internal:', len(internal), 'all_exist:', internal_ok == internal, '| external:', len(external))
    print('zens:', zs, '| contradictions:', len(cons))
    for c in cons:
        print('  -', c.get('type'), '|', (c.get('context_says') or '')[:100], '||', (c.get('output_says') or '')[:100])
