"""测试OpenSERP正确用法"""
import openserp
from openserp import OpenSERP

client = OpenSERP()

print("=== engines 属性 ===")
print(client.engines)
print(type(client.engines))

print("\n=== backend 属性 ===")
print(client.backend)

print("\n=== 尝试 fast_search ===")
try:
    result = client.fast_search("best AI tools 2026", limit=5)
    print(f"结果类型: {type(result)}")
    print(f"结果: {result}")
except Exception as e:
    print(f"fast_search失败: {type(e).__name__}: {e}")

print("\n=== 尝试 any_search ===")
try:
    result = client.any_search("best AI tools 2026", limit=5)
    print(f"结果类型: {type(result)}")
    print(f"结果: {result}")
except Exception as e:
    print(f"any_search失败: {type(e).__name__}: {e}")

print("\n=== 尝试 search (不带engine参数) ===")
try:
    result = client.search("best AI tools 2026", limit=5)
    print(f"结果类型: {type(result)}")
    if hasattr(result, 'results'):
        print(f"结果数: {len(result.results)}")
        for r in result.results[:3]:
            print(f"  - {r.title if hasattr(r, 'title') else r}")
    else:
        print(f"结果: {str(result)[:500]}")
except Exception as e:
    print(f"search失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 尝试 extract (网页正文提取) ===")
try:
    result = client.extract("https://www.futurepedia.io")
    print(f"结果类型: {type(result)}")
    print(f"结果: {str(result)[:500]}")
except Exception as e:
    print(f"extract失败: {type(e).__name__}: {e}")

print("\n=== health ===")
try:
    print(client.health())
except Exception as e:
    print(f"health失败: {e}")

print("\n=== pricing ===")
try:
    print(client.pricing())
except Exception as e:
    print(f"pricing失败: {e}")
