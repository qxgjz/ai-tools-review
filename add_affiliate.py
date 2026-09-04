import json

with open('data/tools.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for tool in data:
    if tool.get('slug') == 'elevenlabs':
        tool['affiliateUrl'] = 'https://try.elevenlabs.io/e45ubw2ct0ag'
        print('已为 ' + tool['name'] + ' 添加联盟链接: ' + tool['affiliateUrl'])
        break

with open('data/tools.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('tools.json 已更新')
