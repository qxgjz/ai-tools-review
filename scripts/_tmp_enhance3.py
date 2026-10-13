# -*- coding: utf-8 -*-
import io, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
p = base + r'\2026-10-10-cursor-vs-windsurf-2026_REWRITE.md'
s = io.open(p, encoding='utf-8').read()

# images after the "Quick Background" section intro
img = """Both official pricing pages, captured in October 2026:

![Cursor pricing plans](/screenshots/real/webp/cursor-pricing.webp)

![Windsurf pricing page (Devin brand)](/screenshots/real/webp/windsurf-pricing.webp)

"""
old = """## Cursor vs Windsurf: Head-to-Head Comparison"""
assert old in s
s = s.replace(old, img + old, 1)

# expand: add feature-by-feature section before FAQ
newsec = """## Feature-by-Feature: Where They Differ in Daily Use

**Tab completion.** Both editors offer AI autocomplete, but Cursor's Tab is the reference implementation — it suggests multi-line edits and anticipates the next logical change, and it is unlimited on paid plans. Windsurf's Tab is unlimited on every plan including free, which is a real advantage if you live in autocomplete and want it at $0. In daily typing, the difference is marginal; both are far ahead of plain VS Code.

**Composer vs Cascade.** Cursor's Composer (and its agent mode) is a chat-driven workflow that can create, edit, and refactor files across your project, with an explicit "accept all" review step. Windsurf's Cascade is more agentic by default: it plans a sequence of steps, executes across multiple files, and can run terminal commands, and on Pro it includes free SWE-2 agent use. If you want the AI to take a task and go run with it, Cascade is the more autonomous of the two; if you want tight control over every edit, Cursor's review-first flow is the safer default.

**Codebase awareness.** Both index your repository, but they differ in depth. Cursor maintains a per-file and repo-level index that powers precise "find the bug in X" queries and context-aware completion. Windsurf's Deep Context feature builds a project-wide understanding for multi-file tasks. In practice, both handle a medium repository well; Cursor's index is more predictable for targeted questions, while Windsurf shines when the task genuinely spans many files.

**Model choice.** Both let you pick among frontier models — Claude, GPT, Gemini, and open-source options. Cursor's model picker is more granular (per-request model switching, custom API keys), while Windsurf routes through its own quota system with the same model family available. For most developers the model flexibility is equivalent; the difference shows up in cost metering.

**Extensions and ecosystem.** This is Cursor's clearest win. As a VS Code fork, Cursor runs the full VS Code extension marketplace — themes, linters, language servers, and tooling work out of the box. Windsurf's ecosystem is younger and, after the Devin rebrand, documentation is split across two names, which makes troubleshooting slightly harder. For beginners and teams standardized on VS Code workflows, this alone justifies choosing Cursor.

**The workflow that decides it.** Our recommendation is to run the same real task on both: take a small bug in your own repository, let each editor's agent fix it, and review the diff. Developers who prefer reviewing precise, smaller diffs tend to stay on Cursor; developers who prefer handing a broad task to the AI and reviewing the outcome tend to prefer Windsurf. That is a preference difference, not a quality difference — which is why we rate them close overall.

## FAQ

### Q: Is Cursor or Windsurf free in 2026?"""
old2 = """## FAQ

### Q: Is Cursor or Windsurf free in 2026?"""
assert old2 in s
s = s.replace(old2, newsec, 1)

io.open(p, 'w', encoding='utf-8').write(s)
words = len(re.findall(r"[A-Za-z0-9']+", s))
imgs = len(re.findall(r'!\[[^\]]*\]\(([^)]+)\)', s))
ints = len(re.findall(r'\[[^\]]*\]\((/blog/[^)]+)\)', s))
exts = len(re.findall(r'\[[^\]]*\]\((https?://[^)]+)\)', s))
print('cursor-vs-windsurf | words:', words, '| imgs:', imgs, '| int:', ints, '| ext:', exts)
