# -*- coding: utf-8 -*-
import io, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    for old, new in pairs:
        assert old in s, path.split('\\')[-1] + ' :: ' + old[:70]
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print(path.split('\\')[-1], 'words:', len(re.findall(r"[A-Za-z][A-Za-z'-]*", s)))

# ---- cursor ----
patch(base + r'\content_drafts\2026-10-11-cursor_ai_review_REWRITE.md', [
    ("It starts free on the Hobby plan, Pro costs $20/month, and Ultra costs $200/month, per the official pricing page we captured.",
     "It starts free on the Hobby plan with no credit card required, Individual plans start at $20/month, Teams cost $40/user/month, and Enterprise is custom-priced, per the official pricing page we captured."),
    ("| Hobby | $0 | 2-week Pro trial, limited AI requests, community support |\n| Pro | $20/month | 500 fast requests, unlimited slow requests, all models |\n| Ultra | $200/month | 2,000 fast requests, priority models, background agents |\n| Teams | Custom | Per-seat billing, shared rules, admin controls |",
     "| Hobby | $0 | No credit card required, limited agent requests, Composer access |\n| Individual | $20/month | Pro/Pro+/Ultra tiers, frontier models, cloud agents, MCPs, skills, hooks, Bugbot |\n| Teams | $40/user/month | Standard/Premium tiers, team billing, SSO, usage analytics, shared marketplace |\n| Enterprise | Custom | Pooled usage, SCIM seat management, audit logs, priority support |"),
    ("The Hobby plan gives you a two-week Pro trial and a small monthly allowance after that, which is enough to evaluate the editor but thin for daily work. Pro at $20/month covers a full-time developer comfortably; Ultra at $200/month is for heavy multi-agent users. The value comparison that matters is against Copilot at $10-50 depending on tier, and the question is not price alone but whether the AI actually accelerates your shipping.",
     "The Hobby plan requires no credit card and includes Composer access with limited agent requests — enough to evaluate the editor but thin for daily work. Individual at $20/month covers a full-time developer comfortably, and the Ultra tier inside Individual serves heavy multi-agent users. The value comparison that matters is against Copilot, whose premium plans run higher than Cursor's $20 Individual tier, and the question is not price alone but whether the AI actually accelerates your shipping."),
    ("For Cursor specifically, Pro at $20/month includes 500 fast requests and unlimited slow requests. Fast requests are the responsive completions you feel in real time; slow requests are background agent work that runs while you keep typing.",
     "For Cursor specifically, Individual at $20/month includes fast requests for real-time responsive work and unlimited slow requests for background agents. Fast requests are the completions you feel while you type; slow requests are agent work that runs while you keep working."),
    ("Hobby is free with a two-week Pro trial, Pro costs $20/month (500 fast requests, unlimited slow requests), and Ultra costs $200/month, per the official pricing page captured October 2026.",
     "Hobby is free with no credit card required, Individual starts at $20/month, Teams at $40/user/month, and Enterprise is custom-priced, per the official pricing page captured October 2026."),
    ("![Cursor code editor interface](/screenshots/real/webp/cursor-code-editor.webp)",
     "![Cursor official documentation page](/screenshots/real/webp/cursor-code-editor.webp)"),
])

# ---- midjourney ----
patch(base + r'\content_drafts\2026-10-11-midjourney-v7-review-2026_REWRITE.md', [
    ("![Midjourney pricing plans](/screenshots/real/webp/midjourney-pricing.webp)",
     "![Midjourney official plans documentation](/screenshots/real/webp/midjourney-plans.webp)"),
    ("![Midjourney gallery output examples](/screenshots/real/webp/midjourney-gallery.webp)",
     "![Midjourney official homepage](/screenshots/real/webp/midjourney-home.webp)"),
    ("| Basic | $10/month | 200 fast generations per month, commercial terms |",
     "| Basic | $10/month | 3.3 hours (200 minutes) of fast GPU time, commercial terms |"),
    ("The pricing model is GPU-time based, which means the plan you need depends on how many images you actually render and whether you use fast or relax mode.",
     "Annual billing cuts every tier by 20% — Basic drops to $96/year, Standard to $288/year, Pro to $576/year, and Mega to $1,152/year, per the same documentation. The pricing model is GPU-time based, which means the plan you need depends on how many images you actually render and whether you use fast or relax mode."),
    ("**Speed.** Fast mode on a Standard plan renders a 1024-square image in roughly a minute, and the relax queue handles bulk work overnight. The tradeoff between speed and cost is explicit and controllable, which is the right design for a tool that bills by GPU time.",
     "**Speed and queue economics.** Fast time is metered per plan — 200 minutes on Basic, 15 hours on Standard, 30 hours on Pro, 60 hours on Mega — while relax mode runs unlimited on Standard and above. The tradeoff between speed and cost is explicit and controllable, which is the right design for a tool that bills by GPU time."),
    ("| Speed | Fast mode ~1 min | Fast | Fast |",
     "| Speed | Fast GPU time metered | Fast | Fast |"),
])

# ---- suno ----
patch(base + r'\content_drafts\2026-10-11-suno-alternatives_REWRITE.md', [
    ("Suno Pro costs $10/month and Premier $30/month, per the official pricing page, but the free tier cuts of 2025 pushed many casual users to these alternatives — Udio's free tier and the credit-light plans of Stable Audio and Loudly now serve that segment best.",
     "Suno Pro costs $10/month and Premier $30/month (annual billing drops them to $8 and $24), per the official pricing page, while the free tier still gives 50 credits per day but excludes downloads and commercial rights — so creators who publish anything are pushed toward paid plans or these alternatives, with Udio's free tier and the credit-light plans of Stable Audio and Loudly serving casual users best."),
    ("![Suno homepage](/screenshots/real/webp/suno.webp)",
     "![Suno official pricing page](/screenshots/real/webp/suno-pricing.webp)"),
    ("The pattern is the same one that hit every generative AI subscription: a generous free tier existed to train users, and once the habit formed, the free credits shrank. Suno's free accounts now receive a small daily allowance instead of the old 50 credits per day, which ends the era of generating a dozen full songs for free.",
     "The pattern is familiar: a free tier exists to train users, and the paid walls sit exactly where creators feel them. Suno's free plan still grants 50 credits per day — enough for a few songs — but it blocks song downloads, excludes commercial rights, and shares the creation queue, which ends the era of casually publishing free-tier output."),
    ("Suno Pro is $10/month with 2,500 credits and Premier is $30/month with 10,000 credits, per the official pricing page. The free tier now offers only a small daily allowance.",
     "Suno Pro is $10/month with 2,500 credits and Premier is $30/month with 10,000 credits, per the official pricing page (annual billing: $8 and $24 per month). The free tier offers 50 credits per day without downloads or commercial rights."),
    ("![Suno music creation interface](/screenshots/real/webp/suno-music-creator.webp)",
     "![Suno official homepage](/screenshots/real/webp/suno-music-creator.webp)"),
])
print('ALL PATCHED')
