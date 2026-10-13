# -*- coding: utf-8 -*-
import io, os, time
from playwright.sync_api import sync_playwright
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
outdir = base + r'\content_drafts\screenshots\batch21'
os.makedirs(outdir, exist_ok=True)
targets = [
    ('devin-home', 'https://devin.ai/', 1440, 900),
    ('devin-pricing', 'https://devin.ai/pricing', 1440, 900),
    ('perplexity-pricing', 'https://www.perplexity.ai/hub/pricing', 1440, 900),
]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={'width': 1440, 'height': 900}, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
    page = ctx.new_page()
    for name, url, w, h in targets:
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=45000)
            page.wait_for_timeout(6000)
            page.screenshot(path=outdir + '\\' + name + '.png', full_page=False)
            print(name, 'OK', url)
        except Exception as e:
            print(name, 'ERR', repr(e)[:200])
    browser.close()
print('done')
