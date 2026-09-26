import json

with open("data/posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# CTR优化：针对排名前10但0点击的文章
updates = {
    "gemini_38_flash_review": {
        "title": "Gemini 3.8 Flash Review (2026): 50 Benchmarks, Real Tests, Honest Verdict",
        "excerpt": "We ran 50 benchmarks on Gemini 3.8 Flash. Is it really the fastest free AI model? See latency, accuracy, and how it compares to GPT-4o and Claude."
    },
    "stable-diffusion-review-2026": {
        "title": "Stable Diffusion Review 2026: Is It Still Worth It? (50+ Images Tested)",
        "excerpt": "We tested Stable Diffusion 3.5 for 4 weeks with 50+ prompts. See image quality, speed, hardware requirements, and if it beats Midjourney in 2026."
    },
    "dify_ai_review": {
        "title": "Dify AI Review 2026: Best Open-Source AI Agent Builder? (Real Hands-On)",
        "excerpt": "We built 3 production apps with Dify AI. Here's our honest review: pros, cons, pricing, limitations, and how it compares to LangChain and Flowise."
    },
    "cursor_ai_review": {
        "title": "Cursor AI Review 2026: I Used It Daily for 3 Months (Honest Take)",
        "excerpt": "After 3 months of daily use, is Cursor still the best AI code editor? We tested coding speed, bug rate, context window, and compared it to Copilot."
    },
    "suno-review-2026": {
        "title": "Suno AI Review 2026: We Made 20 Songs (Is It Worth It?)",
        "excerpt": "We generated 20 songs with Suno v4.5. Here's our honest review: audio quality, genre accuracy, vocal realism, pricing, and alternatives."
    }
}

for post in posts:
    if post["slug"] in updates:
        post["title"] = updates[post["slug"]]["title"]
        post["excerpt"] = updates[post["slug"]]["excerpt"]
        print(f"Updated: {post['slug']}")

with open("data/posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print("Done!")
