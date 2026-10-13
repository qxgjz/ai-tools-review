# -*- coding: utf-8 -*-
import asyncio, os
from playwright.async_api import async_playwright

OUT = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\screenshots\batch16'
os.makedirs(OUT, exist_ok=True)

TARGETS = [
    ('gemini-pricing', 'https://ai.google.dev/pricing'),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={'width': 1440, 'height': 900}, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36')
        page = await ctx.new_page()
        for name, url in TARGETS:
            try:
                await page.goto(url, timeout=45000, wait_until='domcontentloaded')
                await page.wait_for_timeout(5000)
                title = await page.title()
                body = await page.evaluate('document.body ? document.body.innerText.slice(0, 300) : ""')
                print('===', name, '| url:', url, '| title:', title[:100])
                print('body head:', body[:200].replace('\n', ' | '))
                await page.screenshot(path=os.path.join(OUT, name + '.png'))
                print('saved', name + '.png')
            except Exception as e:
                print('===', name, 'ERR', str(e)[:150])
        await browser.close()

asyncio.run(main())
