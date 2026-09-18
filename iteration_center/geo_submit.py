"""
GEO auto-submission script for AIToolCrux.
Submits new/updated URLs to IndexNow and GEO discovery endpoints.
Run: python geo_submit.py [--urls url1 url2 ...]
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

# Config (do not commit real keys to repo - these are read from env or local config)
SITE_URL = "https://www.aitoolcrux.com"
INDEXNOW_KEY = "3f7f80308bcbbd81d91bd93cdc0e1120"
INDEXNOW_KEY_LOC = f"{SITE_URL}/{INDEXNOW_KEY}.txt"

# GEO discovery endpoints (submission-friendly URLs that AI crawlers pick up)
GEO_ENDPOINTS = [
    # IndexNow (Bing/Yandex)
    ("indexnow", "https://api.indexnow.org/indexnow"),
]


def submit_indexnow(urls: list[str]) -> dict:
    """Submit URLs to IndexNow API."""
    payload = {
        "host": "www.aitoolcrux.com",
        "key": INDEXNOW_KEY,
        "keyLocation": INDEXNOW_KEY_LOC,
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "AIToolCrux-GEO/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return {"status": resp.status, "ok": resp.status in (200, 202)}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "ok": False, "error": str(e)}
    except Exception as e:
        return {"status": 0, "ok": False, "error": str(e)}


def get_recent_urls(posts_file: str, days: int = 7) -> list[str]:
    """Get URLs from posts published in last N days."""
    with open(posts_file, "r", encoding="utf-8") as f:
        posts = json.load(f)
    recent = []
    cutoff = datetime.now().replace(hour=0, minute=0, second=0)
    for post in posts:
        date_str = post.get("date", "")
        try:
            post_date = datetime.strptime(date_str[:10], "%Y-%m-%d")
            if (cutoff - post_date).days <= days:
                recent.append(f"{SITE_URL}/blog/{post['slug']}")
        except (ValueError, KeyError):
            continue
    return recent


def main():
    # Determine URLs to submit
    if len(sys.argv) > 2 and sys.argv[1] == "--urls":
        urls = sys.argv[2:]
    else:
        posts_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "ai-tools-review", "data", "posts.json"
        )
        if not os.path.exists(posts_file):
            # Fallback: use sitemap
            urls = [
                f"{SITE_URL}/",
                f"{SITE_URL}/blog",
                f"{SITE_URL}/sitemap.xml",
            ]
        else:
            urls = get_recent_urls(posts_file, days=7)
            # Always include key pages
            urls.extend([
                f"{SITE_URL}/",
                f"{SITE_URL}/blog",
                f"{SITE_URL}/ranking",
            ])
            urls = list(dict.fromkeys(urls))  # dedupe

    print(f"Submitting {len(urls)} URLs to GEO endpoints...")

    results = {}
    for name, endpoint in GEO_ENDPOINTS:
        print(f"  Submitting to {name}...")
        r = submit_indexnow(urls)
        results[name] = r
        print(f"    -> status={r['status']}, ok={r['ok']}")

    # Write log
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "geo_logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"geo_submit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "urls": urls, "results": results}, f, indent=2)
    print(f"\nLog saved to: {log_file}")
    print(f"URLs submitted: {len(urls)}")
    return results


if __name__ == "__main__":
    main()
