#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_llms_full.py — llms-full.txt 文章条目同步脚本（AIToolCrux）
治本方案：文章发布进 data/posts.json 后，运行本脚本即可把缺失的文章条目
追加到 public/llms-full.txt（### Article 格式），保证 AI crawler ingestion 覆盖。
幂等：已存在（按 URL 匹配）的条目跳过，不重复追加。
用法：python scripts/sync_llms_full.py
"""
import json
import re
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / 'data' / 'posts.json'
LLMS = ROOT / 'public' / 'llms-full.txt'
BLOG_BASE = 'https://www.aitoolcrux.com/blog/'


def text_preview(md: str, limit: int = 420) -> str:
    """从 markdown 正文提取纯文本开头（去 frontmatter/标题/图片/代码）。"""
    if not md:
        return ''
    # 去 frontmatter
    md = re.sub(r'\A---\n.*?\n---\n', '', md, flags=re.S)
    # 去代码块
    md = re.sub(r'```.*?```', ' ', md, flags=re.S)
    # 去图片
    md = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', md)
    # 去链接保留文本
    md = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', md)
    # 去标题/强调符
    md = re.sub(r'[#*_>`~|]', ' ', md)
    text = re.sub(r'\s+', ' ', md).strip()
    return text[:limit]


def article_entry(post: dict) -> str:
    title = post.get('title', '').strip()
    slug = post.get('slug', '').strip()
    date = (post.get('date') or post.get('publishedAt') or '').strip()
    author = (post.get('author') or 'AIToolCrux Editorial Team').strip()
    excerpt = (post.get('excerpt') or '').strip()
    preview = text_preview(post.get('content') or '', 420)
    return (
        f'### Article: {title} | AIToolCrux\n'
        f'URL: {BLOG_BASE}{slug}\n'
        f'Date: {date[:10] if date else ""}\n'
        f'Author: {author}\n'
        '\n'
        f'Excerpt: {excerpt}\n'
        '\n'
        f'Content preview: {preview}\n'
    )


def main() -> int:
    posts = json.loads(POSTS.read_text(encoding='utf-8'))
    if not isinstance(posts, list):
        print('ERR: posts.json is not a list'); return 2

    llms = LLMS.read_text(encoding='utf-8')
    existing_urls = set(re.findall(r'^URL: (https://www\.aitoolcrux\.com/blog/[^\s]+)$', llms, flags=re.M))
    added, skipped = [], 0

    for post in posts:
        slug = post.get('slug', '')
        if not slug:
            continue
        url = f'{BLOG_BASE}{slug}'
        if url in existing_urls:
            skipped += 1
            continue
        entry = article_entry(post)
        llms = llms.rstrip('\n') + '\n\n' + entry
        existing_urls.add(url)
        added.append(slug)

    if added:
        LLMS.write_text(llms, encoding='utf-8')

    print(f'POSTS={len(posts)} EXISTING_ENTRIES={len(existing_urls)} ADDED={len(added)} SKIPPED={skipped}')
    for s in added:
        print('  +', s)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
