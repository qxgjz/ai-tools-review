import json

data = json.load(open('data/tools.json', 'r', encoding='utf-8'))

def calc_score(t):
    s = t['scores']
    return s['functionality']*0.25 + s['ux']*0.20 + s['pricing']*0.20 + s['integration']*0.15 + s['support']*0.10 + s['ethics']*0.10

data.sort(key=calc_score, reverse=True)
top10 = data[:10]

print("=== Top 10 Tools Screenshot Status ===")
for i, t in enumerate(top10, 1):
    score = calc_score(t)
    has_screenshots = bool(t.get('screenshots'))
    has_screenshot = bool(t.get('screenshot'))
    has_image = bool(t.get('image'))
    has_images = bool(t.get('images'))
    print(f"{i}. {t['name']} ({t['slug']}) - {score:.1f}/10")
    print(f"   screenshots: {has_screenshots}, screenshot: {has_screenshot}, image: {has_image}, images: {has_images}")
    if t.get('screenshots'):
        print(f"   screenshots count: {len(t['screenshots'])}")
        for j, s in enumerate(t['screenshots'][:3]):
            if isinstance(s, dict):
                print(f"     {j+1}. {s.get('url', s.get('src', 'N/A'))[:80]}")
            else:
                print(f"     {j+1}. {str(s)[:80]}")

# Check all tools for screenshot fields
print("\n=== All Tools Screenshot Field Summary ===")
fields = ['screenshots', 'screenshot', 'image', 'images']
for field in fields:
    count = sum(1 for t in data if t.get(field))
    print(f"{field}: {count}/{len(data)} tools")
