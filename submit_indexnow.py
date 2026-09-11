import json
import requests

# IndexNow configuration
INDEXNOW_KEY = "3f7f80308bcbbd81d91bd93cdc0e1120"
INDEXNOW_URL = "https://api.indexnow.org/IndexNow"
SITE_URL = "https://www.aitoolcrux.com"

# Read tools data
with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

# Read posts data
with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

def calc_score(t):
    s = t['scores']
    return s['functionality']*0.25 + s['ux']*0.20 + s['pricing']*0.20 + s['integration']*0.15 + s['support']*0.10 + s['ethics']*0.10

# Sort tools by score
tools.sort(key=calc_score, reverse=True)

# Build URL list - Top 50 priority pages
urls = []

# 1. Core pages (highest priority)
core_pages = [
    "/",
    "/ranking",
    "/compare",
    "/blog",
    "/about",
    "/contact",
    "/disclosure",
    "/privacy",
    "/terms",
    "/methodology",
]
urls.extend([f"{SITE_URL}{page}" for page in core_pages])

# 2. Top 20 tool pages
for tool in tools[:20]:
    urls.append(f"{SITE_URL}/tools/{tool['slug']}")

# 3. All category pages
categories = list(set(t['category'] for t in tools))
for cat in categories:
    urls.append(f"{SITE_URL}/category/{cat}")

# 4. Latest 10 blog posts
for post in posts[:10]:
    urls.append(f"{SITE_URL}/blog/{post['slug']}")

# Remove duplicates while preserving order
seen = set()
unique_urls = []
for url in urls:
    if url not in seen:
        seen.add(url)
        unique_urls.append(url)

print(f"Total URLs to submit: {len(unique_urls)}")
print("\n=== URL List ===")
for i, url in enumerate(unique_urls, 1):
    print(f"{i}. {url}")

# Submit to IndexNow
print("\n=== Submitting to IndexNow ===")
payload = {
    "host": "www.aitoolcrux.com",
    "key": INDEXNOW_KEY,
    "keyLocation": f"{SITE_URL}/{INDEXNOW_KEY}.txt",
    "urlList": unique_urls
}

try:
    response = requests.post(INDEXNOW_URL, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        print("\n✅ IndexNow submission successful!")
        print("URLs have been submitted to Bing, Yandex, and other participating search engines.")
        print("Google will discover these URLs through normal crawling and sitemap submission.")
    elif response.status_code == 202:
        print("\n✅ IndexNow submission accepted (202).")
        print("The URLs are being processed and will be crawled soon.")
    else:
        print(f"\n⚠️ IndexNow returned status {response.status_code}")
        print("You may need to verify the IndexNow key configuration.")
except Exception as e:
    print(f"\n❌ Error submitting to IndexNow: {e}")
    print("You can manually submit URLs in Google Search Console.")

# Save URL list for manual GSC submission
with open('top50_urls_for_gsc.txt', 'w', encoding='utf-8') as f:
    f.write("=== Top Priority URLs for Google Search Console Indexing ===\n")
    f.write(f"Generated: 2026-09-11\n")
    f.write(f"Total URLs: {len(unique_urls)}\n\n")
    f.write("How to use:\n")
    f.write("1. Go to Google Search Console: https://search.google.com/search-console\n")
    f.write("2. Use the URL Inspection tool at the top\n")
    f.write("3. Paste each URL below and click 'Request indexing'\n")
    f.write("4. Wait for each URL to be processed (usually 1-2 minutes)\n\n")
    f.write("=== URL List ===\n")
    for i, url in enumerate(unique_urls, 1):
        f.write(f"{i}. {url}\n")

print(f"\nURL list saved to: top50_urls_for_gsc.txt")
print("\n=== Next Steps ===")
print("1. IndexNow submission completed (for Bing/Yandex)")
print("2. For Google: manually submit URLs in GSC using the URL Inspection tool")
print("3. Focus on the top 20 URLs first (core pages + top tools)")
print("4. Submit remaining URLs in batches of 10 per day")
