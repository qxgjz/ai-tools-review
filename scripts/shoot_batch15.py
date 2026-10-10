# batch15 screenshot script - real tool pages, 1440x900, headless
# User hard rule: targeted real screenshots, verify each one, NO random/captcha/marketing-homepage images
import os, time
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'content_drafts', 'screenshots', 'batch15')
os.makedirs(OUT, exist_ok=True)

TARGETS = [
    ('perplexity-pricing', 'https://www.perplexity.ai/pricing', 8000),
    ('perplexity-home', 'https://www.perplexity.ai', 8000),
    ('agenta-home', 'https://agenta.ai', 9000),
    ('agenta-pricing', 'https://agenta.ai/pricing', 9000),
    ('chatgpt-pricing', 'https://openai.com/chatgpt/pricing/', 9000),
    ('claude-pricing', 'https://www.anthropic.com/pricing', 9000),
]

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={'width': 1440, 'height': 900},
        user_agent=UA,
        locale='en-US',
    )
    for name, url, wait in TARGETS:
        try:
            page = ctx.new_page()
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(wait)
            # scroll a bit for pricing content
            page.mouse.wheel(0, 400)
            page.wait_for_timeout(1500)
            path = os.path.join(OUT, name + '.png')
            page.screenshot(path=path, full_page=False)
            title = page.title()
            print(name, '| OK | title:', (title or '')[:70])
            page.close()
        except Exception as e:
            print(name, '| FAIL |', str(e)[:120])
            try:
                page.close()
            except Exception:
                pass
    browser.close()
print('done')
