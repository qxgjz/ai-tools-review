import json

with open('lighthouse-report.json', 'r') as f:
    report = json.load(f)

cats = report['categories']
print(f"性能分: {cats['performance']['score'] * 100:.0f}")
print(f"可访问性分: {cats['accessibility']['score'] * 100:.0f}")
print(f"最佳实践分: {cats['best-practices']['score'] * 100:.0f}")
print(f"SEO分: {cats['seo']['score'] * 100:.0f}")

# 看看关键性能指标
audits = report['audits']
print(f"\n关键性能指标:")
print(f"FCP (首次内容绘制): {audits['first-contentful-paint']['displayValue']}")
print(f"LCP (最大内容绘制): {audits['largest-contentful-paint']['displayValue']}")
print(f"TBT (总阻塞时间): {audits['total-blocking-time']['displayValue']}")
print(f"CLS (累积布局偏移): {audits['cumulative-layout-shift']['displayValue']}")
