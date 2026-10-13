import json, sys, inspect
from zens_ink import content_qc

# 看check_draft的签名
print("check_draft签名:", inspect.signature(content_qc.check_draft))
print("check_draft文档:", content_qc.check_draft.__doc__[:500] if content_qc.check_draft.__doc__ else "no doc")

with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

post = posts[0]
content = post['content']
print(f"\n文章长度: {len(content)}")
print(f"文章前200字: {content[:200]}")

# 直接调用试试
try:
    result = content_qc.check_draft(content)
    print(f"\n结果类型: {type(result)}")
    print(f"结果: {str(result)[:1000]}")
except Exception as e:
    print(f"\n调用失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
