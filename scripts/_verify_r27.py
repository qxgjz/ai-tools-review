import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# 1. 旧分类页是否消失
for p in ['out/blog/category/comparison/index.html', 'out/blog/category/guide/index.html']:
    print(p, '存在:', os.path.exists(p))
# 2. 新分类页
for p in ['out/blog/category/comparisons/index.html', 'out/blog/category/guides/index.html']:
    print(p, '存在:', os.path.exists(p))
# 3. sitemap 是否还有单数分类
sm = open('out/sitemap.xml', encoding='utf-8', errors='ignore').read()
print('sitemap含 /blog/category/comparison/:', '/blog/category/comparison/' in sm)
print('sitemap含 /blog/category/guide/:', '/blog/category/guide/' in sm)
print('sitemap含 comparisons:', '/blog/category/comparisons/' in sm)
print('sitemap含 guides:', '/blog/category/guides/' in sm)
# 4. 重定向产物
rd = open('out/_redirects', encoding='utf-8', errors='ignore').read()
print('_redirects含新301:', '/blog/category/comparison /blog/category/comparisons 301' in rd)
