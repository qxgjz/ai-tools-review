import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')

titles = [
 "AI Tools Comparison 2026: Best Tools Compared Side by Side",
 "AI Tools Comparison 2026: Top Tools Ranked by Category",
 "Best AI Tools 2026: Side-by-Side Comparison & Pricing",
]
excerpts = [
 "Compare the best AI tools of 2026 side by side: chatbots, writers, image generators, coding assistants. See pricing, pros, cons, and verdicts to pick your fit.",
 "We tested and compared the top AI tools of 2026 across chat, writing, images, and code. Pricing, pros, cons, and honest verdicts to help you choose.",
]
for t in titles:
    flag = "OK" if 50<=len(t)<=60 else "XX"
    print(f"[{len(t)}c {flag}] {t}")
print()
for e in excerpts:
    flag = "OK" if 120<=len(e)<=155 else "XX"
    print(f"[{len(e)}c {flag}] {e}")
