import json
import os

# 读取工具数据
data = json.load(open('data/tools.json', 'r', encoding='utf-8'))

# 计算评分并排序
def calc_score(scores):
    weights = {
        'functionality': 0.25,
        'ux': 0.20,
        'pricing': 0.20,
        'integration': 0.15,
        'support': 0.10,
        'ethics': 0.10,
    }
    return sum(scores.get(k, 0) * v for k, v in weights.items())

for tool in data:
    tool['_score'] = calc_score(tool['scores'])

# 按评分排序，取Top 50
top_tools = sorted(data, key=lambda x: x['_score'], reverse=True)[:50]

# 按分类分组
from collections import defaultdict
category_tools = defaultdict(list)
for tool in top_tools:
    category_tools[tool['category']].append(tool)

# 分类名称映射
category_names = {
    'chat': 'AI Chat & Assistants',
    'writing': 'AI Writing & Content',
    'image': 'AI Image & Art',
    'code': 'AI Coding & Development',
    'video': 'AI Video & Animation',
    'audio': 'AI Audio & Music',
    'productivity': 'AI Productivity & Office',
    'search': 'AI Search & Research',
    'agent': 'AI Agents & Automation',
    'design': 'AI Design & Creative',
    'dev-tools': 'AI Developer Tools',
    'database': 'AI Database & Vector Store',
    'observability': 'AI Observability & Evaluation',
}

# 生成HTML
html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>2026 AI Tools Guide - Top 50 Tools Reviewed & Rated</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1a202c; background: #f7fafc; }
  .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
  .header { text-align: center; margin-bottom: 50px; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 16px; }
  .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
  .header p { font-size: 1.1rem; opacity: 0.9; }
  .header .badge { display: inline-block; margin-top: 15px; padding: 8px 20px; background: rgba(255,255,255,0.2); border-radius: 20px; font-size: 0.9rem; }
  .toc { background: white; padding: 25px; border-radius: 12px; margin-bottom: 40px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  .toc h2 { font-size: 1.3rem; margin-bottom: 15px; color: #2d3748; }
  .toc ul { list-style: none; columns: 2; column-gap: 30px; }
  .toc li { padding: 5px 0; }
  .toc a { color: #4c51bf; text-decoration: none; }
  .toc a:hover { text-decoration: underline; }
  .category { margin-bottom: 40px; }
  .category h2 { font-size: 1.6rem; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 3px solid #667eea; color: #2d3748; }
  .tool-card { background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); display: flex; justify-content: space-between; align-items: flex-start; }
  .tool-info { flex: 1; }
  .tool-name { font-size: 1.2rem; font-weight: 700; color: #1a202c; margin-bottom: 5px; }
  .tool-vendor { font-size: 0.85rem; color: #718096; margin-bottom: 8px; }
  .tool-desc { font-size: 0.95rem; color: #4a5568; margin-bottom: 8px; }
  .tool-pros { font-size: 0.85rem; color: #38a169; }
  .tool-cons { font-size: 0.85rem; color: #e53e3e; margin-top: 3px; }
  .tool-score { text-align: center; margin-left: 20px; min-width: 70px; }
  .score-number { font-size: 2rem; font-weight: 800; color: #667eea; }
  .score-label { font-size: 0.75rem; color: #718096; text-transform: uppercase; }
  .score-bar { width: 60px; height: 6px; background: #e2e8f0; border-radius: 3px; margin: 5px auto 0; overflow: hidden; }
  .score-fill { height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 3px; }
  .footer { text-align: center; margin-top: 50px; padding: 30px; color: #718096; font-size: 0.9rem; }
  .footer a { color: #667eea; text-decoration: none; }
  @media print {
    body { background: white; }
    .container { padding: 20px; }
    .tool-card { break-inside: avoid; box-shadow: none; border: 1px solid #e2e8f0; }
    .header { background: #667eea !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  }
  @media (max-width: 600px) {
    .header h1 { font-size: 1.8rem; }
    .toc ul { columns: 1; }
    .tool-card { flex-direction: column; }
    .tool-score { margin-left: 0; margin-top: 15px; text-align: left; }
  }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📚 2026 AI Tools Guide</h1>
    <p>Top 50 AI Tools Reviewed, Rated & Compared</p>
    <div class="badge">Based on 6-Dimension Evaluation Framework</div>
  </div>

  <div class="toc">
    <h2>📋 Table of Contents</h2>
    <ul>
'''

# 添加目录
for cat in sorted(category_tools.keys()):
    cat_name = category_names.get(cat, cat.title())
    count = len(category_tools[cat])
    html += f'      <li><a href="#{cat}">{cat_name} ({count})</a></li>\n'

html += '''    </ul>
  </div>
'''

# 添加每个分类的工具
for cat in sorted(category_tools.keys()):
    cat_name = category_names.get(cat, cat.title())
    html += f'  <div class="category" id="{cat}">\n'
    html += f'    <h2>{cat_name}</h2>\n'

    for i, tool in enumerate(category_tools[cat], 1):
        score = tool['_score']
        pros = tool.get('pros', [])[:2]
        cons = tool.get('cons', [])[:1]

        html += f'    <div class="tool-card">\n'
        html += f'      <div class="tool-info">\n'
        html += f'        <div class="tool-name">#{i} {tool["name"]}</div>\n'
        html += f'        <div class="tool-vendor">by {tool.get("vendor", "Unknown")}</div>\n'
        html += f'        <div class="tool-desc">{tool.get("description", "")[:150]}</div>\n'
        if pros:
            html += f'        <div class="tool-pros">✓ {pros[0]}</div>\n'
        if cons:
            html += f'        <div class="tool-cons">✗ {cons[0]}</div>\n'
        html += f'      </div>\n'
        html += f'      <div class="tool-score">\n'
        html += f'        <div class="score-number">{score:.1f}</div>\n'
        html += f'        <div class="score-label">Score</div>\n'
        html += f'        <div class="score-bar"><div class="score-fill" style="width: {score*10}%"></div></div>\n'
        html += f'      </div>\n'
        html += f'    </div>\n'

    html += f'  </div>\n'

html += '''
  <div class="footer">
    <p>Generated by <a href="https://www.aitoolcrux.com">AIToolCrux</a> · September 2026</p>
    <p style="margin-top: 8px;">Scores based on 6-dimension evaluation: Functionality (25%), UX (20%), Pricing (20%), Integration (15%), Support (10%), Ethics (10%)</p>
  </div>
</div>
</body>
</html>
'''

# 确保public目录存在
os.makedirs('public', exist_ok=True)

# 保存HTML文件
output_path = 'public/ai-tools-guide-2026.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'✅ Lead Magnet资源已生成: {output_path}')
print(f'   工具数量: {len(top_tools)}')
print(f'   分类数量: {len(category_tools)}')
print(f'   文件大小: {os.path.getsize(output_path) / 1024:.1f} KB')
print(f'\n访问URL: https://www.aitoolcrux.com/ai-tools-guide-2026.html')
