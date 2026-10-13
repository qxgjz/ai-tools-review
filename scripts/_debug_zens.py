import json, sys
sys.path.insert(0, 'scripts')
from zens_ink_toolkit import ZensInkToolkit

with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

zens = ZensInkToolkit()
post = posts[0]
result = zens.content_quality_check(post['content'], keyword=post.get('keyword', ''))
print("返回类型:", type(result))
print("返回keys:", list(result.keys()) if isinstance(result, dict) else "not dict")
print("完整返回:")
print(json.dumps(result, ensure_ascii=False, indent=2)[:2000])
