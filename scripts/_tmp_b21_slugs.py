# -*- coding: utf-8 -*-
import io, json, os
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
slugs = {p.get('slug') for p in posts}
print('posts total:', len(slugs))
# existing verified webp
webp_dir = base + r'\public\screenshots\real\webp'
for f in ['claude-pricing.webp', 'chatgpt-pricing.webp', 'suno-pricing.webp', 'elevenlabs-pricing.webp', 'gemini-pricing.webp']:
    print(f, '->', os.path.exists(os.path.join(webp_dir, f)))
# internal link whitelist check
wanted = ['claude-alternatives-2026', 'chatgpt-alternatives-2026', 'claude-vs-gemini-2026-comparison', 'gemini-vs-chatgpt-2026', 'chatgpt-vs-claude-2026-comparison', 'perplexity-ai-review-2026', 'best-ai-coding-tools-beginners', 'best-ai-tools-for-beginners-2026', 'best-ai-agents-2026', 'ai-agent-vs-chatbot-2026', 'what-is-an-ai-agent', 'how-to-build-an-ai-agent', 'best-ai-video-generators-2026', 'devin-ai-review', 'cursor_ai_review', 'cursor-vs-github-copilot-2026', 'claude-opus-4-vs-gpt-5-2026', 'perplexity-vs-chatgpt-2026', 'elevenlabs-vs-playht-2026', 'midjourney-v7-review-2026', 'suno-alternatives', 'dify-vs-coze-2026-comparison', 'agenta-ai-review-2026', 'midjourney-alternatives-2026', 'best-paid-ai-tools-worth-buying-2026', 'best-ai-comparison-tools-2026']
for w in wanted:
    print(w, '->', w in slugs)
