"""全面测试OpenSERP的能力"""
import openserp
from openserp import OpenSERP, Engine, Backend, SearchResult, ExtractResult

print("=== OpenSERP 版本 ===")
print(openserp.__version__ if hasattr(openserp, '__version__') else 'unknown')

print("\n=== OpenSERP 类的方法 ===")
print([x for x in dir(OpenSERP) if not x.startswith('_')])

print("\n=== Engine 枚举 ===")
print([x for x in dir(Engine) if not x.startswith('_')])

print("\n=== Backend 枚举 ===")
print([x for x in dir(Backend) if not x.startswith('_')])

print("\n=== SearchResult 字段 ===")
print([x for x in dir(SearchResult) if not x.startswith('_')])

print("\n=== ExtractResult 字段 ===")
print([x for x in dir(ExtractResult) if not x.startswith('_')])

print("\n=== 其他重要类 ===")
others = [x for x in dir(openserp) if x[0].isupper() and x not in ['OpenSERP', 'Engine', 'Backend', 'SearchResult', 'ExtractResult']]
print(others)

print("\n=== 尝试实例化并搜索 ===")
try:
    client = OpenSERP()
    print("实例化成功")
    print("client方法:", [x for x in dir(client) if not x.startswith('_')])
    
    # 尝试搜索
    print("\n尝试搜索 'best AI tools 2026'...")
    result = client.search("best AI tools 2026", engine=Engine.GOOGLE, limit=5)
    print(f"搜索结果类型: {type(result)}")
    print(f"搜索结果: {result}")
except Exception as e:
    print(f"失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
