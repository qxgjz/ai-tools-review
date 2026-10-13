import json, sys, tempfile, re, traceback
from pathlib import Path
from zens_ink import content_qc

with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

post = posts[0]
content = post['content']
title = post['title']

print(f"文章: {post['slug']}")
print(f"内容长度: {len(content)}")

# 保存临时文件
tmp_dir = tempfile.mkdtemp(prefix='zens_debug_')
tmp_file = Path(tmp_dir) / "test.md"
text_content = re.sub(r'<[^>]+>', '', content)
text_content = re.sub(r'&nbsp;', ' ', text_content)
tmp_file.write_text(f"# {title}\n\n{text_content}", encoding='utf-8')
print(f"临时文件: {tmp_file}")
print(f"临时文件大小: {tmp_file.stat().st_size}")

# 调用
try:
    result = content_qc.check_draft(tmp_file)
    print(f"\n成功! 结果类型: {type(result)}")
    print(f"结果keys: {list(result.keys()) if isinstance(result, dict) else 'not dict'}")
    print(f"结果: {str(result)[:2000]}")
except Exception as e:
    print(f"\n失败: {type(e).__name__}: {e}")
    traceback.print_exc()
