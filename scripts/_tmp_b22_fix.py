# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

p1 = base + r'\content_drafts\2026-10-13-ai-video-generator-credits-burn-fast-2026_NEW.md'
s1 = io.open(p1, encoding='utf-8').read()
s1 = s1.replace('| Pika Free | 0 (packs only) | $0 | One-off packs only | Pack-based access |',
                '| Pika Free | 0 (packs) | $0 | One-off packs | Pack-based access |')
io.open(p1, 'w', encoding='utf-8').write(s1)
print('a1 table fixed')

p3 = base + r'\content_drafts\2026-10-13-runway-vs-pika-2026_REWRITE.md'
s3 = io.open(p3, encoding='utf-8').read()
s3 = s3.replace('Both tools include commercial licenses at paid tiers, so the differentiator is workflow fit and billable output, exactly as the keep-vs-cut rule from the SaaS founders applies to every category.',
                'Commercial licenses come with both paid tiers, so the differentiator is workflow fit and billable output, exactly as the keep-vs-cut rule from the SaaS founders applies to every category.')
s3 = s3.replace('Both include commercial licenses at paid tiers with no watermark. Pika\'s volume parallel generation suits social and short-form commercial output.',
                'Paid tiers on both tools include commercial licenses and watermark-free export. Pika\'s volume parallel generation suits social and short-form commercial output.')
io.open(p3, 'w', encoding='utf-8').write(s3)
print('a3 fixed')
