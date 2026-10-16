import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open(r'iteration_center/state.json', encoding='utf-8'))
for i in d['next_iteration_focus']:
    if i.get('id') in ('CF-20261017-001', 'CF-20261017-002', 'GA4-20261017-003'):
        print('=' * 60)
        for k, v in i.items():
            print(f'{k}: {v}')
