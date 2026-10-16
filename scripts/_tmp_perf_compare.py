import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
c = open('out/compare/index.html', encoding='utf-8', errors='ignore').read()
print('HTML大小:', round(len(c)/1024,1), 'KB')
js = re.findall(r'<script[^>]+src="([^"]+)"', c)
css = re.findall(r'<link[^>]+href="([^"]+)"', c)
total = len(c)
for u in js + css:
    p = 'out' + u.split('?')[0]
    if os.path.exists(p):
        sz = os.path.getsize(p)
        total += sz
        print(' ', u, round(sz/1024,1), 'KB')
print('JS总数:', len(js), 'CSS总数:', len(css), '总传输(估):', round(total/1024,1), 'KB')
# 图片检查
imgs = re.findall(r'<img[^>]+src="([^"]+)"[^>]*loading="([^"]*)"', c)
print('img带loading:', len(imgs))
imgs_noload = re.findall(r'<img[^>]+src="([^"]+)"', c)
print('img总数:', len(imgs_noload))
