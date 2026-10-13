# -*- coding: utf-8 -*-
import os
from playwright.sync_api import sync_playwright
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
outdir = base + r'\content_drafts\screenshots\batch22'
os.makedirs(outdir, exist_ok=True)
targets = [
    ('runway-home', 'https://runwayml.com/', 'runway-home.png'),
    ('runway-pricing', 'https://runwayml.com/pricing', 'runway-pricing.png'),
    ('pika-pricing', 'https://pika.art/pricing', 'pika-pricing.png'),
    ('sora-home', 'https://sora.com/', 'sora-home.png'),
    ('hailuo-home', 'https://hailuoai.video/', 'hailuo-home.png'),
]
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
    for name, url, fn in targets:
        pg = ctx.new_page()
        try:
            pg.goto(url, timeout=45000, wait_until='domcontentloaded')
            pg.wait_for_timeout(6000)
            pg.screenshot(path=os.path.join(outdir, fn), full_page=False)
            print(name, 'OK ->', fn)
        except Exception as e:
            print(name, 'FAIL:', str(e)[:120])
        pg.close()
    ctx.close(); b.close()
