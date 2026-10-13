# -*- coding: utf-8 -*-
import io, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
files = ['2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md',
         '2026-10-10-agenta-ai-review-2026_DRAFT.md',
         '2026-10-10-cursor-vs-windsurf-2026_REWRITE.md']
for fn in files:
    p = base + '\\' + fn
    s = io.open(p, encoding='utf-8').read()
    # rename heading
    s = s.replace('## FAQ\n', '## Frequently Asked Questions\n', 1)
    # convert "### Q: xxx" -> "### xxx" and strip leading "A: " from answer paragraph
    def fix_q(m):
        return '### ' + m.group(1).strip()
    s = re.sub(r'### Q: (.+)', fix_q, s)
    # remove "A: " at start of answer paragraphs (line starts with "A: ")
    lines = s.split('\n')
    out = []
    for ln in lines:
        if ln.startswith('A: '):
            out.append(ln[3:])
        else:
            out.append(ln)
    s = '\n'.join(out)
    io.open(p, 'w', encoding='utf-8').write(s)
    print(fn, 'fixed')
