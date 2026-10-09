#!/usr/bin/env python3
"""验证文章草稿结构（字数/H2/链接/图片/FAQ/BLUF）"""
import re
import sys

def check(path):
    text = open(path, encoding='utf-8').read()
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    h2 = re.findall(r'^## (.+)$', text, re.M)
    q = [h for h in h2 if h.strip().endswith('?')]
    faq = 'Frequently Asked' in text
    links = re.findall(r'\]\((https?://[^)]+)\)', text)
    ilinks = re.findall(r'\]\((/[^)]+)\)', text)
    imgs = re.findall(r'!\[[^\]]*\]\([^)]*\)', text)
    bluf = bool(re.search(r'(Bottom line|TL;DR|Key takeaway)', text[:3000]))
    lists = bool(re.search(r'^\s*[-*+]\s', text, re.M))
    print(f'== {path}')
    print(f'words: {len(words)}')
    print(f'H2 count: {len(h2)}')
    print(f'question headings: {q}')
    print(f'FAQ block: {faq}')
    print(f'outbound ({len(links)}): {links}')
    print(f'internal ({len(ilinks)}): {ilinks}')
    print(f'imgs ({len(imgs)}): {imgs}')
    print(f'BLUF: {bluf}')
    print(f'lists: {lists}')
    print()

if __name__ == '__main__':
    for p in sys.argv[1:]:
        check(p)
