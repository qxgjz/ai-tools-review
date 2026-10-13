# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
p1 = base + r'\content_drafts\2026-10-13-ai-video-generator-credits-burn-fast-2026_NEW.md'
s1 = io.open(p1, encoding='utf-8').read()
s1 = s1.replace('Using the official October 2026 pricing as the baseline:',
                'The official pricing snapshot, arranged by tier:')
s1 = s1.replace('By pure credit-per-dollar on October 2026 official pricing, Runway Max at $76/month for 9,500 credits (with one-month rollover) and Pika Fancy at $95/month for 8,550 credits (unlimited parallel) lead the heavy tier; Hailuo\'s 3,000-credit new-user bonus is the best free entry.',
                'By credit-per-dollar on the captured pricing pages, Runway Max at $76/month for 9,500 credits (with one-month rollover) and Pika Fancy at $95/month for 8,550 credits (unlimited parallel) lead the heavy tier; Hailuo\'s 3,000-credit new-user bonus is the best free entry.')
s1 = s1.replace('Yes — Runway Free offers 125 credits/month, Pika Free works on one-off packs, and Hailuo gives new users 3,000 free credits. These are enough to validate prompts and styles before subscribing.',
                'Yes — free rungs exist on all three tools: Runway\'s 125 monthly credits, Pika\'s one-off packs, and Hailuo\'s 3,000-credit new-user bonus. These are enough to validate prompts and styles before subscribing.')
io.open(p1, 'w', encoding='utf-8').write(s1)
print('a1 done')
