# -*- coding: utf-8 -*-
"""
全站 JSON-LD 批量校验（P0）
- 抓取 sitemap.xml 全部 URL
- 校验 FAQPage/Article/BreadcrumbList/Product schema 必填字段
- 输出错误清单到 iteration_center/jsonld_audit_results.md
"""
import json, re, urllib.request, concurrent.futures, time, os
from datetime import datetime

SITEMAP = 'https://www.aitoolcrux.com/sitemap.xml'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jsonld_audit_results.md')
UA = {'User-Agent': 'Mozilla/5.0 AIToolCrux-arch-jsonld-audit'}

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None

def get_sitemap_urls():
    xml = fetch(SITEMAP, timeout=60)
    if not xml:
        return []
    return re.findall(r'<loc>\s*(https?://[^<]+?)\s*</loc>', xml)

def extract_jsonld(html):
    """提取页面内 JSON-LD 块（<script type="application/ld+json">）"""
    blocks = re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S)
    out = []
    for b in blocks:
        try:
            data = json.loads(b.strip())
            if isinstance(data, list):
                out.extend(data)
            else:
                out.append(data)
        except Exception:
            pass
    return out

def validate_schema(page_url, data):
    """返回错误列表 [(type, msg)]"""
    errs = []
    for s in data:
        if not isinstance(s, dict):
            continue
        t = s.get('@type')
        if isinstance(t, list):
            t = t[0]
        t = str(t)
        if t == 'FAQPage':
            if 'mainEntity' not in s:
                errs.append(('FAQPage', '缺 mainEntity'))
            else:
                qs = s['mainEntity'] if isinstance(s['mainEntity'], list) else [s['mainEntity']]
                for i, q in enumerate(qs):
                    if not q.get('name') or not q.get('acceptedAnswer', {}).get('text'):
                        errs.append(('FAQPage', f'mainEntity[{i}] 缺 name/acceptedAnswer.text'))
        elif t == 'Article':
            for f in ['headline', 'datePublished', 'author']:
                if f not in s:
                    errs.append(('Article', f'缺 {f}'))
            if 'dateModified' not in s:
                errs.append(('Article', '缺 dateModified'))
        elif t == 'BreadcrumbList':
            if 'itemListElement' not in s:
                errs.append(('BreadcrumbList', '缺 itemListElement'))
            else:
                items = s['itemListElement'] if isinstance(s['itemListElement'], list) else [s['itemListElement']]
                for i, it in enumerate(items):
                    if not it.get('item', {}).get('name') or not it.get('item', {}).get('@id'):
                        errs.append(('BreadcrumbList', f'item[{i}] 缺 item.name/@id'))
        elif t == 'Product':
            for f in ['name', 'offers']:
                if f not in s:
                    errs.append(('Product', f'缺 {f}'))
            # 关键：Product 缺 affiliate 标记检查（offers 是否含 affiliate 相关）
            offers = s.get('offers', {})
            if isinstance(offers, list):
                offers = offers[0] if offers else {}
            if not offers.get('price') and not offers.get('url'):
                errs.append(('Product', 'offers 缺 price/url'))
    return errs

def check_one(url):
    html = fetch(url)
    if html is None:
        return (url, 'FETCH_FAIL', '抓取失败/超时')
    data = extract_jsonld(html)
    if not data:
        return (url, 'NO_JSONLD', '无 JSON-LD 块')
    errs = []
    types = set()
    for s in data:
        if not isinstance(s, dict):
            continue
        t = s.get('@type')
        if isinstance(t, list):
            t = t[0]
        types.add(str(t))
        errs.extend(validate_schema(url, s))
    return (url, 'OK' if not errs else 'SCHEMA_ERR', f'types={sorted(types)}; errors={errs[:5]}')

def main():
    t0 = time.time()
    urls = get_sitemap_urls()
    print(f'sitemap URLs: {len(urls)}')
    if not urls:
        print('获取 sitemap 失败')
        return

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(check_one, u): u for u in urls}
        for i, f in enumerate(concurrent.futures.as_completed(futs), 1):
            results.append(f.result())
            if i % 100 == 0:
                print(f'  {i}/{len(urls)} 完成 ({time.time()-t0:.0f}s)')

    fetch_fail = [r for r in results if r[1] == 'FETCH_FAIL']
    no_jsonld = [r for r in results if r[1] == 'NO_JSONLD']
    schema_err = [r for r in results if r[1] == 'SCHEMA_ERR']
    ok = [r for r in results if r[1] == 'OK']

    print(f'完成: 总{len(results)}  OK={len(ok)}  SCHEMA_ERR={len(schema_err)}  NO_JSONLD={len(no_jsonld)}  FETCH_FAIL={len(fetch_fail)}')

    # 写报告
    lines = [
        f'# 全站 JSON-LD 审计报告',
        f'',
        f'**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        f'**审计方式**: sitemap 驱动（{len(urls)} URL，10 并发）',
        f'',
        f'| 状态 | 数量 |',
        f'|---|---|',
        f'| OK | {len(ok)} |',
        f'| Schema 错误 | {len(schema_err)} |',
        f'| 无 JSON-LD | {len(no_jsonld)} |',
        f'| 抓取失败 | {len(fetch_fail)} |',
        f'',
        f'## Schema 错误明细（{len(schema_err)}）',
        f'',
    ]
    # 聚合错误类型
    from collections import Counter
    c = Counter()
    for url, st, detail in schema_err:
        for t in re.findall(r"\('(\w+)', '[^']*'\)", detail):
            c[t] += 1
    lines.append('| Schema 类型 | 错误页数 |')
    lines.append('|---|---|')
    for t, n in c.most_common():
        lines.append(f'| {t} | {n} |')
    lines.append('')
    for url, st, detail in schema_err:
        lines.append(f'- {url} → {detail}')
    lines.append('')
    lines.append(f'## 无 JSON-LD 页面（{len(no_jsonld)}）')
    for url, st, detail in no_jsonld[:30]:
        lines.append(f'- {url}')
    lines.append('')
    lines.append(f'## 抓取失败（{len(fetch_fail)}）')
    for url, st, detail in fetch_fail[:20]:
        lines.append(f'- {url}')

    open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))
    print(f'报告已写入: {OUT}')

if __name__ == '__main__':
    main()
