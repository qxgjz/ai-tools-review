# -*- coding: utf-8 -*-
"""batch13 针对性截图拍摄：n8n agents/workflow、OpenAI pricing、ChatGPT 界面"""
import os, time
from playwright.sync_api import sync_playwright

BASE = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
OUT = os.path.join(BASE, 'content_drafts', 'screenshots', 'batch13')
os.makedirs(OUT, exist_ok=True)

targets = [
    # (name, url, wait_ms)
    ('n8n-agents-page', 'https://n8n.io/', 9000),
    ('n8n-workflow-template', 'https://n8n.io/workflows/7158-beginner-manager-agent-with-sub-agent-tools/', 9000),
    ('chatgpt-pricing', 'https://openai.com/chatgpt/pricing/', 9000),
    ('chatgpt-app', 'https://chatgpt.com/', 8000),
    ('claude-pricing', 'https://claude.com/pricing', 9000),
    ('gemini-pricing', 'https://one.google.com/explore', 8000),
]

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36')
    for name, url, wait in targets:
        pg = ctx.new_page()
        try:
            pg.goto(url, timeout=45000, wait_until='domcontentloaded')
            pg.wait_for_timeout(wait)
            path = os.path.join(OUT, name + '.png')
            pg.screenshot(path=path, full_page=False)
            print('OK', name, os.path.getsize(path))
        except Exception as e:
            print('ERR', name, str(e)[:80])
        pg.close()
    b.close()
print('done')
