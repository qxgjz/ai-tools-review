# -*- coding: utf-8 -*-
import os
from playwright.sync_api import sync_playwright
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
out_dir = base + r'\content_drafts\screenshots\batch18'
targets = [
    ('lovable-pricing', 'https://lovable.dev/pricing'),
    ('bolt-pricing', 'https://bolt.new/pricing'),
]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={'width': 1440, 'height': 900},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        locale='en-US',
    )
    page = ctx.new_page()
    for name, url in targets:
        path = os.path.join(out_dir, name + '.png')
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=40000)
            page.wait_for_timeout(3500)
            page.screenshot(path=path, full_page=False)
            print(name, 'OK', url)
        except Exception as e:
            print(name, 'ERR', str(e)[:100])
    browser.close()
