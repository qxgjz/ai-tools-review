import json
with open('iteration_center/hallucination_audit_report.json', 'r', encoding='utf-8') as f:
    report = json.load(f)
print('总检查:', report['total'])
print('前5篇详情:')
for r in report['all_results'][:5]:
    print(f"  {r['slug']}: score={r['score']}, hallucination={r['hallucination']}, warnings={r['warnings']}, len={r['content_length']}")
print('\n随机抽3篇:')
import random
for r in random.sample(report['all_results'], 3):
    print(f"  {r['slug']}: score={r['score']}, len={r['content_length']}, warnings={r['warnings'][:2]}")
