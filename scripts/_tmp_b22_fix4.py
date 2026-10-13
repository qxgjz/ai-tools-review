# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
p1 = base + r'\content_drafts\2026-10-13-ai-video-generator-credits-burn-fast-2026_NEW.md'
s1 = io.open(p1, encoding='utf-8').read()
s1 = s1.replace('Verified monthly plans at a glance:',
                'Monthly allowance and price, side by side:')
s1 = s1.replace('### Which AI video plan is the best value?',
                '### How do I choose the right subscription size?')
io.open(p1, 'w', encoding='utf-8').write(s1)
print('a1 retitled again')
