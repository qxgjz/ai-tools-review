# -*- coding: utf-8 -*-
"""r37 职责A：竞品缓存 vs 本地内容缺口对比"""
import json, os, re, glob

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
cache = json.load(open(P + r'\iteration_center\competitor_sitemap_cache.json', encoding='utf-8'))
fp_cats = cache['sites']['futurepedia']['categories']  # 75
print('futurepedia 75 categories:')
for c in fp_cats:
    print(' ', c)

# 本地 content_drafts 全量
drafts = glob.glob(P + r'\content_drafts\**\*.md', recursive=True)
local = []
for f in drafts:
    base = os.path.basename(f).lower()
    local.append(base)
print()
print('local drafts:', len(local))

# 主题词提取（从文件名去 slug 结构）
def tokens(name):
    n = re.sub(r'\.md$', '', name)
    n = re.sub(r'^(published[\\/_])', '', n)
    n = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', n)
    n = re.sub(r'_?READY$', '', n)
    return n

local_tokens = [tokens(b) for b in local]
# 关键词映射：竞品分类 -> 本地是否覆盖（检查本地文件名是否含分类主题词）
syn = {
    '3d-generator': ['3d'], 'ai-agent': ['agent'], 'ai-assistant': ['assistant'],
    'ai-content-detector': ['detector', 'detection'], 'ai-detector': ['detector', 'detection'],
    'ai-education': ['education', 'teacher'], 'ai-fashion': ['fashion'],
    'ai-image-generator': ['image-generator', 'text-to-image', 'image gen'],
    'ai-search-engine': ['search-engine'], 'ai-video-generator': ['video-gen', 'text-to-video'],
    'art': ['art'], 'avatar': ['avatar'], 'cartoon': ['cartoon'], 'chatbot': ['chatbot'],
    'code-assistant': ['code-assistant', 'coding', 'copilot'], 'copywriting': ['copywrit'],
    'customer-support': ['customer'], 'design': ['design'], 'developer-tools': ['developer'],
    'email-assistant': ['email'], 'finance': ['finance'], 'gaming': ['game'],
    'grammar-checker': ['grammar'], 'healthcare': ['health'], 'hr': ['hr'],
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
    'email-marketing': ['email'], 'ads-generator': ['ads', 'ad-generator'],
    'blog-generator': ['blog'], 'character': ['character'], 'data-analysis': ['data'],
    'interview': ['interview'], 'landing-page': ['landing'], 'lms': ['lms'],
    'market-research': ['market-research'], 'mockup': ['mockup'], 'mp3': ['mp3', 'song', 'lyric'],
    'quiz': ['quiz'], 'workflow': ['workflow'], '2d-generator': ['2d'],
    'animation': ['anim'], 'art-generator': ['art'], 'background-remover': ['remove-background', 'bg-remove'],
    'browser-extension': ['extension'], 'celebrity': ['celebrity'], 'children': ['children', 'kids'],
    'clip-maker': ['clip'], 'code-review': ['code-review'], 'comic': ['comic'],
    'contract': ['contract'], 'creative-writing': ['creative'], 'database': ['database'],
    'ecommerce': ['ecommerce', 'shopify'], 'education-assistant': ['education'], 'emoji': ['emoji'],
    'grammar': ['grammar'], 'image-editing': ['image-edit', 'photo-edit', 'canva'], 'japanese': ['japanese'],
    'music-sheet': ['music-sheet'], 'nft': ['nft'], 'poem': ['poem'], 'quotes': ['quote'],
    'screenwriting': ['screenwrit', 'script'], 'self-care': ['self-care'], 'text-based': ['text'],
    'undress': ['undress'], 'video-editing': ['video-edit', 'capcut'], 'wiki': ['wiki'],
}

gaps = []
for c in fp_cats:
    kws = syn.get(c, [c.lower()])
    hit = any(any(k in lt for k in kws) for lt in local_tokens)
    if not hit:
        gaps.append(c)
print()
print('缺口分类（竞品有/本地无）:', len(gaps))
for g in gaps:
    print('  ', g)
