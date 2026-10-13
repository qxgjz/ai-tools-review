# -*- coding: utf-8 -*-
"""抓取标杆网站HTML用于设计解剖"""
import urllib.request
import ssl
import os
import time

sites = {
    "linear": "https://linear.app",
    "vercel": "https://vercel.com",
    "futurepedia": "https://www.futurepedia.io",
    "theresanaiforthat": "https://theresanaiforthat.com",
    "topai": "https://topai.tools",
    "framer": "https://framer.com",
}
outdir = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\design_research'
os.makedirs(outdir, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

for name, url in sites.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
            data = resp.read()
        path = os.path.join(outdir, name + '.html')
        with open(path, 'wb') as f:
            f.write(data)
        print('%s OK %d bytes (final url: %s)' % (name, len(data), resp.geturl()))
    except Exception as e:
        print('%s FAIL %s' % (name, e))
    time.sleep(1)
