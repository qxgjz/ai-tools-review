import json
import os

# 文章数
posts = json.load(open('data/posts.json', 'r', encoding='utf-8'))
print(f'文章总数: {len(posts)}')

# 截图数（递归统计）
screenshots_dir = 'public/screenshots'
screenshot_count = 0
for root, dirs, files in os.walk(screenshots_dir):
    for f in files:
        if f.endswith(('.png', '.jpg', '.webp', '.svg')):
            screenshot_count += 1
print(f'截图总数: {screenshot_count}')

# 工具数
tools = json.load(open('data/tools.json', 'r', encoding='utf-8'))
print(f'工具总数: {len(tools)}')

# 迭代轮次
state = json.load(open('iteration_center/state.json', 'r', encoding='utf-8'))
print(f'迭代轮次: {state.get("current_round", "未知")}')
print(f'已完成任务数: {len(state.get("completed_tasks", []))}')
