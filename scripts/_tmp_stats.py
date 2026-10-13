# -*- coding: utf-8 -*-
import re, io, sys, os
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
for fn in sys.argv[1:]:
    p = os.path.join(base, fn)
    s = io.open(p, encoding='utf-8').read()
    words = len(re.findall(r"[A-Za-z0-9']+", s))
    faqs = len(re.findall(r'^### ', s, re.M))
    imgs = len(re.findall(r'!\[[^\]]*\]\(([^)]+)\)', s))
    ints = re.findall(r'\[[^\]]*\]\((/blog/[^)]+)\)', s)
    exts = re.findall(r'\[[^\]]*\]\((https?://[^)]+)\)', s)
    print(fn, '| words:', words, '| faq:', faqs, '| imgs:', imgs, '| int:', len(ints), '| ext:', len(exts))
