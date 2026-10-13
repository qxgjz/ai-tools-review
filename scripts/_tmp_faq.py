# -*- coding: utf-8 -*-
import io, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
for fn in ['2026-10-10-what-is-an-ai-agent_DRAFT.md', '2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md']:
    s = io.open(base + '\\' + fn, encoding='utf-8').read()
    m = re.search(r'## FAQ.*?(?=\n## |\Z)', s, re.S)
    print('===', fn)
    if m:
        print(m.group(0)[:600])
    print()
