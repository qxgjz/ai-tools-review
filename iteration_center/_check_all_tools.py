# -*- coding: utf-8 -*-
"""检查所有SEO工具真实安装状态"""
import importlib, sys, subprocess, json

tools = {
    "zens-ink": ("zens_ink", None),
    "Crawl4AI": ("crawl4ai", None),
    "trafilatura": ("trafilatura", None),
    "textstat": ("textstat", None),
    "openserp": ("openserp", None),
    "playwright": ("playwright", None),
    "googleapiclient": ("googleapiclient", None),
    "google-analytics-data": ("google.analytics.data_v1beta", None),
    "nltk": ("nltk", None),
    "tiktoken": ("tiktoken", None),
    "rank_bm25": ("rank_bm25", None),
    "courlan": ("courlan", None),
    "llmevalkit": ("llmevalkit", None),
    "opengtm": ("opengtm", None),
    "chromadb": ("chromadb", None),
    "playwright-stealth": ("playwright_stealth", None),
    "patchright": ("patchright", None),
}

results = {}
for name, (mod, _) in tools.items():
    try:
        m = importlib.import_module(mod)
        ver = getattr(m, "__version__", "?")
        results[name] = f"✅ {ver}"
    except Exception as e:
        results[name] = f"❌ {type(e).__name__}: {str(e)[:60]}"

# broken-link-checker (npm)
try:
    r = subprocess.run(["npx", "broken-link-checker", "--version"], capture_output=True, text=True, timeout=15)
    results["broken-link-checker"] = f"✅ {r.stdout.strip() or r.stderr.strip()[:40]}"
except Exception as e:
    results["broken-link-checker"] = f"❌ {e}"

# lighthouse (npm)
try:
    r = subprocess.run(["npx", "lighthouse", "--version"], capture_output=True, text=True, timeout=15)
    results["lighthouse"] = f"✅ {r.stdout.strip()}"
except Exception as e:
    results["lighthouse"] = f"❌ {e}"

for k, v in results.items():
    print(f"{k:25s} {v}")

# 检查项目脚本是否存在
import os
proj = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
scripts_to_check = [
    "scripts/quality_audit.py", "real_seo_audit.py", "real_geo_aeo_audit.py",
    "real_internal_link_audit.py", "seo_technical_check.py",
    "iteration_center/keyword_miner.py", "scripts/llmevalkit_toolkit.py",
    "scripts/opengtm_toolkit.py", "generate_real_article.py",
    "scripts/run_hallucination_detect.py",
]
print("\n=== 项目脚本存在性 ===")
for s in scripts_to_check:
    p = os.path.join(proj, s)
    print(f"{'✅' if os.path.exists(p) else '❌'} {s}")
