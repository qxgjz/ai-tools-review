"""测试zens-ink正确用法 + 检查所有已有脚本功能"""
import os
os.environ['SERPER_API_KEY'] = 'db3bbe31d1470d3d4358896851c04030d2e76a6e'

# 1. 测试site_audit正确用法
print("=== site_audit 模块方法 ===")
from zens_ink import site_audit
print([x for x in dir(site_audit) if not x.startswith('_')])

print("\n=== onpage_audit 模块方法 ===")
from zens_ink import onpage_audit
print([x for x in dir(onpage_audit) if not x.startswith('_')])

print("\n=== content_qc.check_draft 测试 ===")
from zens_ink import content_qc
test_content = """# Test Article
This is a test article about AI tools. It has some content.

## Quick Answer
AI tools are great.

## Key Takeaways
- Point 1
- Point 2

## FAQ
### What is AI?
AI is artificial intelligence.
"""
try:
    result = content_qc.check_draft(test_content)
    print(f"结果类型: {type(result)}")
    print(f"结果: {result}")
except Exception as e:
    print(f"失败: {type(e).__name__}: {e}")

print("\n=== content_qc.grade 测试 ===")
try:
    result = content_qc.grade(test_content)
    print(f"结果: {result}")
except Exception as e:
    print(f"失败: {type(e).__name__}: {e}")

# 2. 检查项目根目录所有Python脚本
print("\n=== 项目根目录所有Python脚本 ===")
import glob
scripts = glob.glob('*.py') + glob.glob('scripts/*.py') + glob.glob('iteration_center/*.py') + glob.glob('.github/scripts/*.py')
for s in sorted(scripts):
    size = os.path.getsize(s)
    # 读取前5行看功能
    try:
        with open(s, 'r', encoding='utf-8') as f:
            first_lines = [f.readline().strip() for _ in range(5)]
        desc = ' | '.join([l for l in first_lines if l and not l.startswith('#!/')][:2])
    except:
        desc = ''
    print(f"  {s} ({size}B) - {desc[:80]}")
