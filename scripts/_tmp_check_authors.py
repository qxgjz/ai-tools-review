import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
c = open('out/authors/aitoolcrux-editorial-team/index.html', encoding='utf-8', errors='ignore').read()
print('KB:', round(len(c) / 1024, 1))
scripts = re.findall(r'<script[^>]*>(.*?)</script>', c, re.S)
scripts.sort(key=len, reverse=True)
s0 = scripts[0]
print('biggest script KB:', round(len(s0) / 1024, 1))
print('has content key:', '"content"' in s0)
print('has faq key:', '"faq"' in s0)
print('has slug key:', '"slug"' in s0)
print('has excerpt key:', '"excerpt"' in s0)
# 找 RSC 里 post 对象的样例片段
idx = s0.find('AIToolCrux')
print('sample around AIToolCrux:', s0[idx:idx+200].replace('\n', ' ')[:200])
