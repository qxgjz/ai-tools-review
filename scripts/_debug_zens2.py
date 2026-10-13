import json, sys
sys.path.insert(0, 'scripts')

# 直接用zens-ink原生API
from zens_ink import content_qc
print("content_qc模块方法:", [m for m in dir(content_qc) if not m.startswith('_')])

# 试试直接调用
with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

post = posts[0]
content = post['content']
keyword = post.get('keyword', '')

# 看看有什么可用函数
for func_name in ['check', 'evaluate', 'score', 'qc', 'analyze_content', 'quality_check']:
    if hasattr(content_qc, func_name):
        print(f"\n找到函数: {func_name}")
        try:
            result = getattr(content_qc, func_name)(content, keyword)
            print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)[:1000]}")
        except Exception as e:
            print(f"调用失败: {e}")
