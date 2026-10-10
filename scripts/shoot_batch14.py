"""batch14: Playwright screenshots for voice changers + coding tools articles.
Targets: real product/pricing pages only. No marketing homepages, no 404, no captcha.
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

OUT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\screenshots\batch14"
os.makedirs(OUT, exist_ok=True)

TARGETS = [
    # (name, url, wait_selector, scroll)
    ("elevenlabs-voice-changer", "https://elevenlabs.io/voice-changer", "body", False),
    ("cursor-pricing", "https://www.cursor.com/pricing", "body", False),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width":1440,"height":900}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
        for name, url, sel, scroll in TARGETS:
            page = await ctx.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=45000)
                await page.wait_for_timeout(4000)
                try:
                    await page.wait_for_selector(sel, timeout=8000)
                except Exception:
                    pass
                if scroll:
                    await page.mouse.wheel(0, 500)
                    await page.wait_for_timeout(1500)
                path = os.path.join(OUT, name + ".png")
                await page.screenshot(path=path, full_page=False)
                print("OK", name, os.path.getsize(path))
            except Exception as e:
                print("FAIL", name, str(e)[:120])
            finally:
                await page.close()
        await browser.close()

asyncio.run(main())
