"""测试zens-ink的site_audit和onpage_audit"""
import os
os.environ['SERPER_API_KEY'] = 'db3bbe31d1470d3d4358896851c04030d2e76a6e'

from zens_ink import site_audit, onpage_audit, content_matrix, content_qc

print("=== site_audit.run 测试 ===")
try:
    # 测试单个URL
    result = site_audit.run('https://www.aitoolcrux.com')
    print(f"结果类型: {type(result)}")
    if isinstance(result, dict):
        print(f"keys: {list(result.keys())[:20]}")
        # 打印检查结果
        for k, v in result.items():
            if isinstance(v, (int, float, str, bool)):
                print(f"  {k}: {v}")
            elif isinstance(v, list):
                print(f"  {k}: {len(v)} items")
            elif isinstance(v, dict):
                print(f"  {k}: {len(v)} keys")
    else:
        print(str(result)[:1000])
except Exception as e:
    print(f"失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n=== onpage_audit.audit_page 测试 ===")
try:
    result = onpage_audit.audit_page('https://www.aitoolcrux.com')
    print(f"结果类型: {type(result)}")
    print(str(result)[:1000])
except Exception as e:
    print(f"失败: {type(e).__name__}: {e}")

print("\n=== content_matrix 模块 ===")
print([x for x in dir(content_matrix) if not x.startswith('_')])

print("\n=== content_qc 模块 ===")
print([x for x in dir(content_qc) if not x.startswith('_')])
