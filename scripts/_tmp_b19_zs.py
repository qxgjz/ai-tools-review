# -*- coding: utf-8 -*-
import io, json, re, subprocess, sys
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, base)
files = {
    'clearscope-alternatives': base + r'\content_drafts\2026-10-12-clearscope-alternatives_REWRITE.md',
    'gemini_38_flash_review': base + r'\content_drafts\2026-10-12-gemini_38_flash_review_REWRITE.md',
    'dify-vs-langchain-2026': base + r'\content_drafts\2026-10-12-dify-vs-langchain-2026_REWRITE.md',
}
from scripts.llmevalkit_toolkit import LMEvalKit
for slug, path in files.items():
    md = io.open(path, encoding='utf-8').read()
    out = subprocess.run([sys.executable, '-m', 'zens_ink.content_qc', path, '--format', 'json'], capture_output=True, text=True, encoding='utf-8')
    try:
        res = json.loads(out.stdout)
        score = res[0]['score'] if isinstance(res, list) else res.get('score')
    except Exception:
        score = 'ERR:' + out.stdout[:120] + out.stderr[:120]
    words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", md))
    faq = len(re.findall(r'^### ', md, re.M))
    h2 = len(re.findall(r'^## ', md, re.M))
    internal = len(re.findall(r'\]\(/blog/', md))
    external = len(re.findall(r'\]\(https://(?!www\.aitoolcrux)', md))
    imgs = len(re.findall(r'!\[[^\]]*\]\(/screenshots/', md))
    ev = LMEvalKit().evaluate_content(md, keyword=slug.replace('_','-'), context=md)
    print(slug, '| zens-ink:', score, '| words:', words, '| H2:', h2, '| FAQ:', faq, '| imgs:', imgs, '| internal:', internal, '| external:', external, '| llmevalkit:', ev)
