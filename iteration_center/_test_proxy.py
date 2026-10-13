# -*- coding: utf-8 -*-
import os, requests, time
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"

print("[1] via proxy:")
t = time.time()
try:
    r = requests.get("https://oauth2.googleapis.com/", timeout=10)
    print(f"    OK status={r.status_code} elapsed={time.time()-t:.1f}s")
except Exception as e:
    print(f"    FAIL {type(e).__name__}: {str(e)[:200]}")

print("[2] direct (no proxy):")
t = time.time()
try:
    r = requests.get("https://oauth2.googleapis.com/", timeout=6, proxies={"http": None, "https": None})
    print(f"    OK status={r.status_code} elapsed={time.time()-t:.1f}s")
except Exception as e:
    print(f"    FAIL {type(e).__name__}: {str(e)[:200]}")
