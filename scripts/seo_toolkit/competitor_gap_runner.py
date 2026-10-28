# -*- coding: utf-8 -*-
"""
竞品 sitemap 抓取前置环境检测 + 缓存（SOP 动作3+4）
- 前置检测：zens_ink 可导入 + 网络连通（优先代理 7890，代理不可用自动回退直连）
- 在线：运行 zens_ink.competitor_gap，成功后把竞品 /ai-tools/ 分类清单缓存到
        iteration_center/competitor_sitemap_cache.json
- 离线：明确报 [ENV ERROR]，不静默降级；如有缓存则回退读取缓存并退出码 3
- 网络通道：输出 CHANNEL=proxy|direct；direct 表示 Clash 7890 未运行已自动回退直连

用法:
  python scripts/seo_toolkit/competitor_gap_runner.py            # 完整流程
  python scripts/seo_toolkit/competitor_gap_runner.py --check-only  # 只做环境检测

退出码:
  0 = 成功（含缓存命中回退）
  2 = zens_ink 模块缺失（环境错误）
  3 = 网络不可用且无缓存（环境错误；直连也失败时才报此码）
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
CHANNEL = 'unknown'  # proxy|direct，实测通道


def _fetch(url, timeout):
    """请求 url：优先代理 7890，代理失败自动回退直连。

    urllib 的 ProxyHandler 不做自动回退：代理不可达时 open() 直接抛错。
    实测（r72）：Clash 7890 未运行时脚本误报 [ENV ERROR] 网络不可用，
    即使直连可用也无法抓取；且对代理根路径发探测 GET 会被 HTTP 代理拒绝，
    必须把"实际请求失败→回退直连"做成请求级 fallback。"""
    global CHANNEL
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY}))
        resp = opener.open(req, timeout=timeout)
        CHANNEL = 'proxy'
        return resp
    except Exception:
        CHANNEL = 'direct'
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}))  # {} = 禁用代理，直连
        return opener.open(
            urllib.request.Request(url, headers={'User-Agent': UA}),
            timeout=timeout)


def check_zens_ink():
    try:
        import zens_ink  # noqa: F401
        return True
    except ImportError:
        return False


def check_network(timeout=12):
    try:
        _fetch('https://futurepedia.io/sitemap.xml', timeout).close()
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
    with _fetch(url, timeout) as resp:
        xml = resp.read().decode('utf-8', errors='ignore')
    return extract_categories(xml)


def main():
    check_only = '--check-only' in sys.argv
    print('=== competitor sitemap runner ===')
    zens_ok = check_zens_ink()
    net_ok = check_network()
    print(f'zens_ink 可导入: {zens_ok}')
    print(f'网络通道: {CHANNEL}（proxy=走7890 / direct=代理不可用已回退直连）')
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
            print(f'  {name}: 抓取失败 - {e}（通道={CHANNEL}，若为 direct 且仍失败说明直连也不通，需开启 Clash 或检查网络）')
    save_cache(cache_data)
    print(f'[OK] 竞品 sitemap 分类清单已缓存: {CACHE_PATH}')
    sys.exit(0)


if __name__ == '__main__':
    main()
