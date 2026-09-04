"""
使用reportlab生成2026 AI工具指南PDF
包含Top 50工具，按分类组织
"""
import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white, gray
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# 加载工具数据
with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

# 计算总分
def calculate_score(scores):
    weights = {
        'functionality': 0.25,
        'ux': 0.20,
        'pricing': 0.20,
        'integration': 0.15,
        'support': 0.10,
        'ethics': 0.10,
    }
    total = 0
    for dim, weight in weights.items():
        val = scores.get(dim, 0)
        if isinstance(val, (int, float)):
            total += val * weight
    return round(total, 1)

# 按总分排序，取Top 50
tools_with_score = []
for tool in tools:
    score = calculate_score(tool.get('scores', {}))
    tools_with_score.append({
        'name': tool.get('name', 'Unknown'),
        'vendor': tool.get('vendor', 'Unknown'),
        'category': tool.get('category', 'other'),
        'description': tool.get('description', '')[:100],
        'score': score,
        'pros': tool.get('pros', [])[:2],
        'cons': tool.get('cons', [])[:2],
    })

tools_with_score.sort(key=lambda x: x['score'], reverse=True)
top_50 = tools_with_score[:50]

# 按分类分组
categories = {}
for tool in top_50:
    cat = tool['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(tool)

# 分类名称映射
CATEGORY_NAMES = {
    'chat': 'AI Chat & Assistants',
    'writing': 'AI Writing & Content',
    'image': 'AI Image & Art',
    'code': 'AI Coding & Development',
    'video': 'AI Video & Animation',
    'audio': 'AI Audio & Music',
    'productivity': 'AI Productivity',
    'search': 'AI Search & Research',
    'agent': 'AI Agents & Automation',
    'agent-framework': 'AI Agent Frameworks',
    'agent-runtime': 'AI Agent Runtimes',
    'rag': 'RAG & Retrieval',
    'memory': 'AI Memory & Knowledge',
    'design': 'AI Design & Creative',
    'dev-tools': 'Developer Tools',
    'database': 'Database & Vector',
    'observability': 'AI Observability',
}

# 创建PDF
output_path = 'public/2026-ai-tools-guide.pdf'
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2.5*cm,
    bottomMargin=2.5*cm,
)

# 样式
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontSize=24,
    textColor=HexColor('#1a56db'),
    alignment=TA_CENTER,
    spaceAfter=20,
)

subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Normal'],
    fontSize=14,
    textColor=HexColor('#374151'),
    alignment=TA_CENTER,
    spaceAfter=30,
)

h1_style = ParagraphStyle(
    'CustomH1',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=HexColor('#1e40af'),
    spaceBefore=20,
    spaceAfter=12,
)

h2_style = ParagraphStyle(
    'CustomH2',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=HexColor('#374151'),
    spaceBefore=12,
    spaceAfter=8,
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    textColor=HexColor('#374151'),
    alignment=TA_JUSTIFY,
)

small_style = ParagraphStyle(
    'CustomSmall',
    parent=styles['Normal'],
    fontSize=8,
    leading=10,
    textColor=HexColor('#6b7280'),
)

# 构建内容
story = []

# 封面
story.append(Spacer(1, 3*cm))
story.append(Paragraph("2026 AI Tools Guide", title_style))
story.append(Paragraph("Top 50 AI Tools Evaluated by 6-Dimension Scoring", subtitle_style))
story.append(Spacer(1, 1*cm))

# 评分说明
story.append(Paragraph("About This Guide", h1_style))
story.append(Paragraph(
    "This guide features the top 50 AI tools evaluated by AIToolCrux using our "
    "proprietary 6-dimension scoring framework: Functionality (25%), User Experience (20%), "
    "Pricing & Value (20%), Integration (15%), Support (10%), and Ethics & Transparency (10%). "
    "Each tool receives a total score out of 10, with higher scores indicating better overall performance.",
    body_style
))
story.append(Spacer(1, 0.5*cm))

# 目录
story.append(Paragraph("Table of Contents", h1_style))
toc_data = [["Category", "Tools"]]
for cat, cat_tools in sorted(categories.items()):
    cat_name = CATEGORY_NAMES.get(cat, cat.title())
    toc_data.append([cat_name, str(len(cat_tools))])

toc_table = Table(toc_data, colWidths=[10*cm, 4*cm])
toc_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a56db')),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e5e7eb')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f9fafb')]),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
]))
story.append(toc_table)
story.append(PageBreak())

# 每个分类的工具
for cat, cat_tools in sorted(categories.items()):
    cat_name = CATEGORY_NAMES.get(cat, cat.title())
    story.append(Paragraph(f"{cat_name} ({len(cat_tools)} tools)", h1_style))

    for i, tool in enumerate(cat_tools, 1):
        # 工具卡片
        tool_content = []

        # 工具名称和评分
        header_data = [[
            Paragraph(f"<b>{i}. {tool['name']}</b>", h2_style),
            Paragraph(f"<b>Score: {tool['score']}/10</b>", h2_style),
        ]]
        header_table = Table(header_data, colWidths=[11*cm, 4*cm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        tool_content.append(header_table)

        # 厂商和描述
        tool_content.append(Paragraph(
            f"<b>Vendor:</b> {tool['vendor']}",
            small_style
        ))
        tool_content.append(Spacer(1, 0.2*cm))
        tool_content.append(Paragraph(tool['description'], body_style))
        tool_content.append(Spacer(1, 0.2*cm))

        # 优缺点
        if tool['pros']:
            pros_text = " | ".join(tool['pros'])
            tool_content.append(Paragraph(
                f"<b>Pros:</b> {pros_text}",
                small_style
            ))
        if tool['cons']:
            cons_text = " | ".join(tool['cons'])
            tool_content.append(Paragraph(
                f"<b>Cons:</b> {cons_text}",
                small_style
            ))

        tool_content.append(Spacer(1, 0.5*cm))

        # 保持工具卡片在一起
        story.append(KeepTogether(tool_content))

    story.append(PageBreak())

# 页脚
story.append(Paragraph("About AIToolCrux", h1_style))
story.append(Paragraph(
    "AIToolCrux is an independent AI tool evaluation platform. We use a transparent "
    "6-dimension scoring framework to evaluate AI tools objectively. Our evaluations are "
    "based on hands-on testing, community feedback, and continuous monitoring. "
    "Visit https://www.aitoolcrux.com for the latest reviews and comparisons.",
    body_style
))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(
    "Disclaimer: This guide is for informational purposes only. Tool scores reflect our "
    "evaluation at the time of publication and may change as tools evolve. Always verify "
    "current pricing and features on the official website before making a purchase decision.",
    small_style
))

# 生成PDF
doc.build(story)

# 检查文件大小
file_size = os.path.getsize(output_path)
file_size_kb = file_size / 1024

print(f"✅ PDF生成成功: {output_path}")
print(f"   文件大小: {file_size_kb:.1f} KB")
print(f"   包含工具: {len(top_50)} 个")
print(f"   分类数: {len(categories)} 个")
