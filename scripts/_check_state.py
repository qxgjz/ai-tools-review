import json

with open('iteration_center/state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

print("state.json keys:", list(state.keys()))
print("\nnext_iteration_focus类型:", type(state.get('next_iteration_focus')))
if isinstance(state.get('next_iteration_focus'), list):
    print("当前待办数:", len(state['next_iteration_focus']))
    if state['next_iteration_focus']:
        print("第一条待办keys:", list(state['next_iteration_focus'][0].keys()))
        print("第一条示例:", json.dumps(state['next_iteration_focus'][0], ensure_ascii=False, indent=2)[:500])
elif isinstance(state.get('next_iteration_focus'), dict):
    print("next_iteration_focus keys:", list(state['next_iteration_focus'].keys()))
