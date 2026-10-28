# -*- coding: utf-8 -*-
"""r38 竞品 sitemap 实抓（requests 带 UA）+ 缺口复核"""
import requests, json, re, os
from datetime import datetime, timezone

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'}
PROXIES = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
now = datetime.now(timezone.utc).isoformat()

def fetch(url):
    r = requests.get(url, headers=UA, proxies=PROXIES, timeout=30)
    return r.text if r.status_code == 200 else None

def parse_categories(text):
    locs = re.findall(r'<loc>(.*?)</loc>', text, re.S)
    cats = set()
    for l in locs:
        m = re.search(r'/ai-tools/([^/]+)/?$', l)
        if m: cats.add(m.group(1).lower())
    return sorted(cats), len(locs)

# 实抓 futurepedia
fp_text = fetch('https://futurepedia.io/sitemap.xml')
fp_cats, fp_total = parse_categories(fp_text) if fp_text else ([], 0)
print('futurepedia sitemap:', 'OK' if fp_text else 'FAIL', '| urls:', fp_total, '| categories:', len(fp_cats))

# 更新缓存
cache_p = os.path.join(P, 'iteration_center', 'competitor_sitemap_cache.json')
cache = json.load(open(cache_p, encoding='utf-8')) if os.path.exists(cache_p) else {'sites': {}}
cache['cached_at'] = now
cache['source'] = 'live_fetch_20261028_requests_ua'
cache['sites']['futurepedia'] = {'url': 'https://futurepedia.io/sitemap.xml', 'categories': fp_cats}
json.dump(cache, open(cache_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('cache updated ->', len(fp_cats), 'categories')

# 缺口复核（本地 content_drafts）
import glob
drafts = glob.glob(P + r'\content_drafts\**\*.md', recursive=True)
local = [os.path.basename(f).lower() for f in drafts]
syn = {
    '3d-generator': ['3d'], 'ai-agent': ['agent'], 'ai-assistant': ['assistant'],
    'ai-content-detector': ['detector', 'detection'], 'ai-detector': ['detector', 'detection'],
    'ai-education': ['education', 'teacher'], 'ai-fashion': ['fashion'],
    'ai-image-generator': ['image-generator', 'text-to-image'], 'ai-search-engine': ['search-engine'],
    'ai-video-generator': ['video-gen', 'text-to-video'], 'art': ['art'], 'avatar': ['avatar'],
    'cartoon': ['cartoon'], 'chatbot': ['chatbot'], 'code-assistant': ['code-assistant', 'coding', 'copilot'],
    'copywriting': ['copywrit'], 'customer-support': ['customer'], 'design': ['design'],
    'developer-tools': ['developer'], 'email-assistant': ['email'], 'finance': ['finance'],
    'gaming': ['game'], 'grammar-checker': ['grammar'], 'healthcare': ['health'], 'hr': ['hr'],
    'legal': ['legal'], 'logo-generator': ['logo'], 'marketing': ['market'],
    'meeting-assistant': ['meeting'], 'music-generator': ['music', 'suno', 'udio'],
    'note-taking': ['note'], 'paraphraser': ['paraphrase'], 'photo-editing': ['photo', 'edit'],
    'podcast': ['podcast'], 'presentation': ['presentation', 'slide'], 'productivity': ['productiv'],
    'programming': ['program'], 'real-estate': ['real-estate'], 'religion': ['religion'],
    'research': ['research'], 'resume': ['resume', 'cover-letter'], 'sales': ['sales'],
    'seo': ['seo'], 'social-media': ['social-media', 'instagram'], 'spreadsheet': ['spreadsheet', 'excel'],
    'story-teller': ['story'], 'summarizer': ['summar'], 'text-to-speech': ['text-to-speech', 'tts', 'voice'],
    'transcription': ['transcri'], 'travel': ['travel'], 'video-enhancer': ['video-enhanc'],
    'voiceover': ['voiceover', 'voice-over'], 'website-builder': ['website', 'site-builder'],
    'writing': ['writing', 'essay'], 'youtube': ['youtube', 'thumbnail'],
}
gaps = [c for c in fp_cats if not any(any(k in lt for k in syn.get(c, [c.lower()])) for lt in local)]
print('gap categories:', len(gaps))
for g in gaps: print('  ', g)
