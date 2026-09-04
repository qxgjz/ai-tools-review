"""
使用reportlab生成2026 AI工具指南PDF
包含封面、目录、按分类组织的Top 50工具
"""

import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    ListFlowable, ListItem, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# 配置
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "public", "2026-ai-tools-guide.pdf")
TOOLS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tools.json")

# 颜色配置
PRIMARY_COLOR = HexColor("#1a56db")
SECONDARY_COLOR = HexColor("#0e9f6e")
DARK_COLOR = HexColor("#1f2937")
LIGHT_GRAY = HexColor("#f3f4f6")
GOLD_COLOR = HexColor("#f59e0b")

# 分类名称映射
CATEGORY_NAMES = {
    "chat": "AI Chat & Assistants",
    "writing": "AI Writing & Content",
    "image": "AI Image & Art",
    "code": "AI Coding & Dev",
    "video": "AI Video & Animation",
    "audio": "AI Audio & Music",
    "productivity": "AI Productivity",
    "search": "AI Search & Research",
    "agent": "AI Agents & Automation",
    "design": "AI Design & Creative",
    "dev-tools": "AI Developer Tools",
    "database": "AI Database & Vector",
    "observability": "AI Observability",
}


def calculate_score(scores):
    """计算六维加权总分"""
    weights = {
        "functionality": 0.25,
        "ux": 0.20,
        "pricing": 0.20,
        "integration": 0.15,
        "support": 0.10,
        "ethics": 0.10,
    }
    total = 0
    for dim, weight in weights.items():
        val = scores.get(dim, 5)
        if isinstance(val, (int, float)):
            total += val * weight
    return round(total, 1)


def get_grade(score):
    """获取等级"""
    if score >= 9.0:
        return "S"
    elif score >= 8.0:
        return "A"
    elif score >= 7.0:
        return "B"
    elif score >= 6.0:
        return "C"
    else:
        return "D"


def create_styles():
    """创建自定义样式"""
    styles = getSampleStyleSheet()

    # 封面标题
    styles.add(ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontSize=36,
        leading=42,
        alignment=TA_CENTER,
        textColor=PRIMARY_COLOR,
        spaceAfter=20,
        fontName="Helvetica-Bold",
    ))

    # 封面副标题
    styles.add(ParagraphStyle(
        name="CoverSubtitle",
        parent=styles["Normal"],
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor=DARK_COLOR,
        spaceAfter=10,
    ))

    # 章节标题
    styles.add(ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading1"],
        fontSize=22,
        leading=28,
        textColor=PRIMARY_COLOR,
        spaceBefore=20,
        spaceAfter=15,
        fontName="Helvetica-Bold",
    ))

    # 工具名称
    styles.add(ParagraphStyle(
        name="ToolName",
        parent=styles["Heading2"],
        fontSize=16,
        leading=20,
        textColor=DARK_COLOR,
        spaceBefore=12,
        spaceAfter=6,
        fontName="Helvetica-Bold",
    ))

    # 工具描述
    styles.add(ParagraphStyle(
        name="ToolDesc",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor=HexColor("#4b5563"),
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    ))

    # 标签文字
    styles.add(ParagraphStyle(
        name="LabelText",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=HexColor("#6b7280"),
    ))

    # 目录项
    styles.add(ParagraphStyle(
        name="TOCItem",
        parent=styles["Normal"],
        fontSize=12,
        leading=18,
        textColor=DARK_COLOR,
        leftIndent=20,
    ))

    return styles


def create_cover(styles):
    """创建封面"""
    elements = []

    # 顶部空白
    elements.append(Spacer(1, 2 * inch))

    # 主标题
    elements.append(Paragraph("2026 AI Tools Guide", styles["CoverTitle"]))

    # 副标题
    elements.append(Paragraph("Top 50 AI Tools Evaluated by 6-Dimension Scoring", styles["CoverSubtitle"]))

    elements.append(Spacer(1, 0.5 * inch))

    # 评分模型说明
    score_info = """
    <b>Scoring Model:</b> Functionality (25%) · UX (20%) · Pricing (20%) · 
    Integration (15%) · Support (10%) · Ethics (10%)
    """
    elements.append(Paragraph(score_info, styles["CoverSubtitle"]))

    elements.append(Spacer(1, 1 * inch))

    # 网站信息
    elements.append(Paragraph("www.aitoolcrux.com", styles["CoverSubtitle"]))
    elements.append(Paragraph("Independent AI Tool Reviews & Comparisons", styles["LabelText"]))

    elements.append(PageBreak())
    return elements


def create_toc(styles, categories_with_tools):
    """创建目录"""
    elements = []

    elements.append(Paragraph("Table of Contents", styles["SectionTitle"]))
    elements.append(Spacer(1, 0.3 * inch))

    # 封面和介绍
    elements.append(Paragraph("1. Introduction & Scoring Methodology", styles["TOCItem"]))
    elements.append(Spacer(1, 0.1 * inch))

    # 各分类
    for i, (cat_slug, cat_name, tools) in enumerate(categories_with_tools, 2):
        elements.append(Paragraph(
            f"{i}. {cat_name} ({len(tools)} tools)",
            styles["TOCItem"]
        ))

    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph("Appendix: How to Use This Guide", styles["TOCItem"]))

    elements.append(PageBreak())
    return elements


def create_intro(styles):
    """创建介绍页"""
    elements = []

    elements.append(Paragraph("Introduction & Scoring Methodology", styles["SectionTitle"]))

    intro_text = """
    Welcome to the 2026 AI Tools Guide! This comprehensive guide features the top 50 AI tools
    across multiple categories, each evaluated using our proprietary 6-dimension scoring model.
    Our goal is to help you find the perfect AI tool for your specific needs, whether you're a
    content creator, developer, marketer, or business professional.
    """
    elements.append(Paragraph(intro_text, styles["ToolDesc"]))
    elements.append(Spacer(1, 0.3 * inch))

    # 评分维度表
    elements.append(Paragraph("<b>6-Dimension Scoring Model</b>", styles["ToolName"]))

    score_data = [
        ["Dimension", "Weight", "What We Evaluate"],
        ["Functionality", "25%", "Core features, output quality, use case coverage"],
        ["User Experience", "20%", "Interface design, learning curve, documentation quality"],
        ["Pricing & Value", "20%", "Cost transparency, free tier, ROI"],
        ["Integration", "15%", "API quality, platform compatibility, ecosystem"],
        ["Support & Reliability", "10%", "Uptime, update frequency, customer support"],
        ["Ethics & Transparency", "10%", "Data privacy, bias disclosure, responsible AI"],
    ]

    score_table = Table(score_data, colWidths=[1.8 * inch, 0.8 * inch, 3.4 * inch])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#d1d5db")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(score_table)

    elements.append(Spacer(1, 0.3 * inch))

    # 等级说明
    grade_text = """
    <b>Grade Scale:</b> S (9.0+) · A (8.0-8.9) · B (7.0-7.9) · C (6.0-6.9) · D (below 6.0)
    """
    elements.append(Paragraph(grade_text, styles["ToolDesc"]))

    elements.append(PageBreak())
    return elements


def create_tool_section(styles, cat_slug, cat_name, tools):
    """创建一个分类的工具列表"""
    elements = []

    elements.append(Paragraph(cat_name, styles["SectionTitle"]))
    elements.append(Spacer(1, 0.2 * inch))

    for tool in tools:
        score = calculate_score(tool.get("scores", {}))
        grade = get_grade(score)

        # 工具信息表格
        tool_data = [
            [
                Paragraph(f"<b>{tool['name']}</b>", styles["ToolName"]),
                Paragraph(f"<b>{grade}</b>", ParagraphStyle(
                    "GradeBadge",
                    parent=styles["Normal"],
                    fontSize=14,
                    alignment=TA_CENTER,
                    textColor=white,
                )),
                Paragraph(f"<b>{score}/10</b>", ParagraphStyle(
                    "ScoreText",
                    parent=styles["Normal"],
                    fontSize=12,
                    alignment=TA_CENTER,
                    textColor=PRIMARY_COLOR,
                )),
            ],
        ]

        tool_table = Table(tool_data, colWidths=[4.0 * inch, 0.8 * inch, 1.2 * inch])
        tool_table.setStyle(TableStyle([
            ("BACKGROUND", (1, 0), (1, 0), GOLD_COLOR if grade == "S" else (
                SECONDARY_COLOR if grade == "A" else PRIMARY_COLOR if grade == "B" else
                HexColor("#f59e0b") if grade == "C" else HexColor("#ef4444")
            )),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(tool_table)

        # 厂商和分类
        vendor_text = f"<b>Vendor:</b> {tool.get('vendor', 'N/A')} &nbsp;&nbsp; <b>Category:</b> {cat_name}"
        elements.append(Paragraph(vendor_text, styles["LabelText"]))
        elements.append(Spacer(1, 0.05 * inch))

        # 描述
        desc = tool.get("description", "")
        if desc:
            elements.append(Paragraph(desc[:300] + ("..." if len(desc) > 300 else ""), styles["ToolDesc"]))

        # 优缺点
        pros = tool.get("pros", [])
        cons = tool.get("cons", [])

        if pros or cons:
            pc_data = []
            if pros:
                pros_text = "<b>Pros:</b><br/>" + "<br/>".join([f"• {p}" for p in pros[:3]])
            else:
                pros_text = "<b>Pros:</b> N/A"

            if cons:
                cons_text = "<b>Cons:</b><br/>" + "<br/>".join([f"• {c}" for c in cons[:3]])
            else:
                cons_text = "<b>Cons:</b> N/A"

            pc_data.append([
                Paragraph(pros_text, styles["ToolDesc"]),
                Paragraph(cons_text, styles["ToolDesc"]),
            ])

            pc_table = Table(pc_data, colWidths=[3.0 * inch, 3.0 * inch])
            pc_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 0), (0, 0), HexColor("#f0fdf4")),
                ("BACKGROUND", (1, 0), (1, 0), HexColor("#fef2f2")),
                ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#e5e7eb")),
            ]))
            elements.append(pc_table)

        elements.append(Spacer(1, 0.2 * inch))

    elements.append(PageBreak())
    return elements


def create_appendix(styles):
    """创建附录"""
    elements = []

    elements.append(Paragraph("Appendix: How to Use This Guide", styles["SectionTitle"]))

    appendix_text = """
    <b>1. Identify Your Needs:</b> Start by determining what you primarily need an AI tool for.
    Are you writing content, generating images, writing code, or creating videos?<br/><br/>
    <b>2. Browse by Category:</b> Use the table of contents to navigate to the relevant category.
    Each category contains the top tools in that space.<br/><br/>
    <b>3. Compare Scores:</b> Each tool has a total score out of 10 and a letter grade (S/A/B/C/D).
    Higher scores indicate better overall performance across all 6 dimensions.<br/><br/>
    <b>4. Read Pros and Cons:</b> Every tool includes a list of pros and cons to help you understand
    its strengths and weaknesses for your specific use case.<br/><br/>
    <b>5. Try Before You Buy:</b> Most tools offer free tiers or free trials. We recommend trying
    2-3 top candidates before committing to a paid subscription.<br/><br/>
    <b>6. Stay Updated:</b> The AI tool landscape changes rapidly. Visit www.aitoolcrux.com for
    the latest reviews, comparisons, and updates.
    """
    elements.append(Paragraph(appendix_text, styles["ToolDesc"]))

    elements.append(Spacer(1, 0.5 * inch))

    # 免责声明
    disclaimer = """
    <b>Disclaimer:</b> This guide is for informational purposes only. All scores and evaluations
    are based on our independent testing and research methodology. Product names, logos, and brands
    are property of their respective owners. We may earn affiliate commissions from purchases made
    through links on our website, but this does not influence our evaluations or rankings.
    """
    elements.append(Paragraph(disclaimer, styles["LabelText"]))

    return elements


def main():
    """主函数"""
    print("🚀 开始生成2026 AI工具指南PDF...")

    # 加载工具数据
    with open(TOOLS_PATH, "r", encoding="utf-8") as f:
        tools = json.load(f)

    print(f"📊 加载了 {len(tools)} 个工具")

    # 计算每个工具的总分并排序
    for tool in tools:
        tool["_score"] = calculate_score(tool.get("scores", {}))

    tools_sorted = sorted(tools, key=lambda x: x["_score"], reverse=True)

    # 取Top 50
    top_50 = tools_sorted[:50]
    print(f"⭐ 选取Top 50工具")

    # 按分类分组
    categories_with_tools = []
    for cat_slug, cat_name in CATEGORY_NAMES.items():
        cat_tools = [t for t in top_50 if t.get("category") == cat_slug]
        if cat_tools:
            categories_with_tools.append((cat_slug, cat_name, cat_tools))

    print(f"📂 覆盖 {len(categories_with_tools)} 个分类")

    # 创建样式
    styles = create_styles()

    # 创建文档
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    # 构建内容
    elements = []

    # 封面
    elements.extend(create_cover(styles))

    # 目录
    elements.extend(create_toc(styles, categories_with_tools))

    # 介绍
    elements.extend(create_intro(styles))

    # 各分类工具
    for cat_slug, cat_name, cat_tools in categories_with_tools:
        elements.extend(create_tool_section(styles, cat_slug, cat_name, cat_tools))

    # 附录
    elements.extend(create_appendix(styles))

    # 生成PDF
    doc.build(elements)

    file_size = os.path.getsize(OUTPUT_PATH) / 1024
    print(f"\n✅ PDF生成成功!")
    print(f"📄 文件路径: {OUTPUT_PATH}")
    print(f"📦 文件大小: {file_size:.1f} KB")
    print(f"📊 包含 {len(top_50)} 个工具，覆盖 {len(categories_with_tools)} 个分类")


if __name__ == "__main__":
    main()
