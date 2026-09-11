import json
import os

# 读取工具数据
with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

# 按评分排序取Top20
def get_score(tool):
    scores = tool.get('scores', {})
    if not scores:
        return 0
    numeric_scores = [v for v in scores.values() if isinstance(v, (int, float))]
    return sum(numeric_scores) / len(numeric_scores) if numeric_scores else 0

sorted_tools = sorted(tools, key=get_score, reverse=True)
top20 = sorted_tools[:20]

# 检查截图目录
screenshot_dir = 'public/screenshots'
existing_screenshots = set()
if os.path.exists(screenshot_dir):
    for f in os.listdir(screenshot_dir):
        if f.endswith('.svg') or f.endswith('.png') or f.endswith('.jpg'):
            existing_screenshots.add(os.path.splitext(f)[0])

print("=== Top 20 Tools Screenshot Check ===\n")
missing = []
has_screenshot = 0

for i, tool in enumerate(top20, 1):
    slug = tool.get('slug', '')
    name = tool.get('name', 'Unknown')
    score = get_score(tool)
    has = slug in existing_screenshots
    status = "✅" if has else "❌"
    if has:
        has_screenshot += 1
    else:
        missing.append((i, slug, name, score))
    print(f"{i:2d}. {status} {name:30s} (slug: {slug:25s}, score: {score:.1f})")

print(f"\n=== Summary ===")
print(f"Top20 tools with screenshots: {has_screenshot}/20")
print(f"Missing screenshots: {len(missing)}")

if missing:
    print(f"\n=== Missing Screenshots (need to generate) ===")
    for i, slug, name, score in missing:
        print(f"  {i}. {name} ({slug}) - score: {score:.1f}")
