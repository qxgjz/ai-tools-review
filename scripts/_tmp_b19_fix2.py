# -*- coding: utf-8 -*-
import io
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-12-clearscope-alternatives_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
old = "The entry-price column is intentionally a range, because every vendor publishes current numbers on its own pricing page — link them below and check before purchase."
new = "The entry-price column is intentionally a range, because every vendor publishes current numbers on its own pricing page — [Ahrefs pricing](https://ahrefs.com/pricing), [Surfer SEO pricing](https://surferseo.com/pricing/), and [Frase pricing](https://www.frase.io/pricing/) are the places to check before purchase."
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('patched')
