# -*- coding: utf-8 -*-
"""
竞品 sitemap 抓取前置环境检测 + 缓存（SOP 动作3+4）
- 前置检测：zens_ink 可导入 + 网络连通（代理 7890 或直连）
- 在线：运行 zens_ink.competitor_gap，成功后把竞品 /ai-tools/ 分类清单缓存到
        iteration_center/competitor_sitemap_cache.json
- 离线：明确报 [ENV ERROR]，不静默降级；如有缓存则回退读取缓存并退出码 3

用法:
  python scripts/seo_toolkit/competitor_gap_runner.py            # 完整流程
  python scripts/seo_toolkit/competitor_gap_runner.py --check-only  # 只做环境检测

退出码:
  0 = 成功（含缓存命中回退）
  2 = zens_ink 模块缺失（环境错误）
  3 = 网络不可用且无缓存（环境错误）
  4 = competitor_gap 运行失败
"""
import sys, os, json, re, subprocess, datetime, urllib.request

CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..',
                          'iteration_center', 'competitor_sitemap_cache.json')
SITES = {
    'aitoolcrux': 'https://www.aitoolcrux.com/sitemap.xml',
    'futurepedia': 'https://futurepedia.io/sitemap.xml',
    'topai': 'https://topai.tools/sitemap.xml',
}
PROXY = 'http://127.0.0.1:7890'
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')


def _opener():
    """返回走代理 127.0.0.1:7890 + UA 的 opener；代理不可用时回退直连"""
    handlers = []
    try:
        ph = urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})
        handlers.append(ph)
    except Exception:
        pass
    return urllib.request.build_opener(*handlers)


def check_zens_ink():
    try:
        import zens_ink  # noqa: F401
        return True
    except ImportError:
        return False


def check_network(timeout=12):
    try:
        req = urllib.request.Request('https://futurepedia.io/sitemap.xml',
                                     headers={'User-Agent': UA})
        _opener().open(req, timeout=timeout)
        return True
    except Exception:
        return False


def extract_categories(xml_text):
    cats = set()
    for m in re.finditer(r'<loc>([^<]+)</loc>', xml_text):
        url = m.group(1)
        if '/ai-tools/' in url:
            parts = url.split('/ai-tools/')
            if len(parts) > 1 and parts[1]:
                cat = parts[1].strip('/').split('/')[0]
                if cat and not cat.startswith('?'):
                    cats.add(cat)
    return sorted(cats)


def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, encoding='utf-8') as f:
            return json.load(f)
    return None


def save_cache(data):
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_categories(url, timeout=25):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with _opener().open(req, timeout=timeout) as resp:
        xml = resp.read().decode('utf-8', errors='ignore')
    return extract_categories(xml)


def main():
    check_only = '--check-only' in sys.argv
    print('=== competitor sitemap runner ===')
    zens_ok = check_zens_ink()
    net_ok = check_network()
    print(f'zens_ink 可导入: {zens_ok}')
    print(f'网络连通 (futurepedia sitemap): {net_ok}')

    if not zens_ok:
        print('[ENV ERROR] zens_ink 模块缺失：请先 pip install zens-ink，或在装有依赖的本地环境执行，勿在无依赖快照运行')
        sys.exit(2)
    if not net_ok:
        cache = load_cache()
        print('[ENV ERROR] 网络不可用，尝试回退缓存')
        if cache:
            print(f'  缓存命中 (cached_at={cache.get("cached_at")})')
            for name, info in cache.get('sites', {}).items():
                print(f'  {name}: {len(info.get("categories", []))} 分类')
            print(f'  缓存路径: {CACHE_PATH}')
            sys.exit(0)
        print('[ENV ERROR] 网络不可用且无缓存：本次无法实抓，禁止静默降级/凭记忆分析')
        sys.exit(3)
    if check_only:
        print('[OK] 环境检测通过（zens_ink + 网络）')
        sys.exit(0)

    # 在线：运行 zens_ink.competitor_gap（我们的站 vs futurepedia）
    print('运行 competitor_gap ...')
    try:
        subprocess.run(
            [sys.executable, '-m', 'zens_ink.competitor_gap',
             '--url', SITES['aitoolcrux'], '--compare', SITES['futurepedia']],
            check=True)
    except subprocess.CalledProcessError as e:
        print('[RUN ERROR] competitor_gap 运行失败:', e)
        sys.exit(4)

    # 抓取各站 /ai-tools/ 分类并缓存
    cache_data = {'cached_at': datetime.datetime.now().isoformat(timespec='seconds'), 'sites': {}}
    for name, url in SITES.items():
        try:
            cats = fetch_categories(url)
            cache_data['sites'][name] = {'url': url, 'categories': cats}
            print(f'  {name}: {len(cats)} 分类')
        except Exception as e:
            cache_data['sites'][name] = {'url': url, 'error': str(e)}
            print(f'  {name}: 抓取失败 - {e}')
    save_cache(cache_data)
    print(f'[OK] 竞品 sitemap 分类清单已缓存: {CACHE_PATH}')
    sys.exit(0)


if __name__ == '__main__':
    main()
