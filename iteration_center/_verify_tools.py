# -*- coding: utf-8 -*-
import importlib
tools = {
    "zens-ink": "zens_ink", "tiktoken": "tiktoken", "llmevalkit": "llmevalkit",
    "opengtm": "opengtm", "chromadb": "chromadb", "textstat": "textstat",
    "openserp": "openserp", "playwright": "playwright", "nltk": "nltk",
    "rank_bm25": "rank_bm25", "courlan": "courlan", "trafilatura": "trafilatura",
    "googleapiclient": "googleapiclient", "google-analytics-data": "google.analytics.data_v1beta",
    "Crawl4AI": "crawl4ai", "playwright-stealth": "playwright_stealth",
    "patchright": "patchright",
}
for name, mod in tools.items():
    try:
        m = importlib.import_module(mod)
        v = getattr(m, "__version__", "ok")
        print(f"✅ {name:25s} {v}")
    except Exception as e:
        print(f"❌ {name:25s} {type(e).__name__}: {str(e)[:50]}")
