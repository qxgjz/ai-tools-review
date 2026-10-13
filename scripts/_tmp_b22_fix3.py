# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
p1 = base + r'\content_drafts\2026-10-13-ai-video-generator-credits-burn-fast-2026_NEW.md'
s1 = io.open(p1, encoding='utf-8').read()
s1 = s1.replace('The official pricing snapshot, arranged by tier:',
                'Verified monthly plans at a glance:')
s1 = s1.replace('### Which AI video generator has the most credits for the price?',
                '### Which AI video plan is the best value?')
s1 = s1.replace('### Is there a free AI video generator in 2026?',
                '### What is the cheapest way to start with AI video in 2026?')
io.open(p1, 'w', encoding='utf-8').write(s1)
print('a1 faq retitled')
