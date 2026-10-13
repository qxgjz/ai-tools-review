# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
# first check batch14 FAQ body format
s14 = io.open(base + r'\2026-10-10-what-is-an-ai-agent_DRAFT.md', encoding='utf-8').read()
i = s14.find('## Frequently Asked Questions')
print('--- batch14 FAQ body ---')
print(s14[i:i+500])
