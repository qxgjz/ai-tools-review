#!/usr/bin/env python3
"""
Lead Magnet PDF生成脚本
生成Top 50 AI工具指南PDF
"""

import json
import os
import unicodedata
from fpdf import FPDF

def clean_text(text):
    """清理文本，移除或替换非ASCII字符"""
    if not text:
        return ""
    # 将Unicode字符转换为ASCII等效字符
    text = unicodedata.normalize('NFKD', text)
    # 移除非ASCII字符
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text.strip()

class AIToolsPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, "AIToolCrux - 2026 AI Tools Selection Guide", align="C")
            self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(26, 86, 219)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

    def chapter_body(self, body):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(51, 51, 51)
        self.multi_cell(0, 6, body)
        self.ln()

    def tool_card(self, rank, tool, category):
        # 工具排名和名称
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(26, 86, 219)
        self.cell(0, 8, f"#{rank} {clean_text(tool['name'])}", ln=True)

        # 厂商和分类
        self.set_font("Helvetica", "", 10)
        self.set_text_color(102, 102, 102)
        vendor = clean_text(tool.get("vendor", "Unknown"))
        self.cell(0, 6, f"Vendor: {vendor} | Category: {clean_text(category)}", ln=True)

        # 评分
        scores = tool.get("scores", {})
        if scores:
            total = 0
            weights = {"functionality": 0.25, "ux": 0.20, "pricing": 0.20, "integration": 0.15, "support": 0.10, "ethics": 0.10}
            for key, weight in weights.items():
                if key in scores and isinstance(scores[key], (int, float)):
                    total += scores[key] * weight
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(14, 159, 110)
            self.cell(0, 6, f"Overall Score: {total:.1f}/10", ln=True)

        # 描述
        desc = clean_text(tool.get("description", "No description available."))
        if len(desc) > 200:
            desc = desc[:197] + "..."
        self.set_font("Helvetica", "", 10)
        self.set_text_color(51, 51, 51)
        self.multi_cell(0, 5, desc)

        # 优缺点
        pros = tool.get("pros", [])
        cons = tool.get("cons", [])
        if pros:
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(14, 159, 110)
            self.cell(0, 5, "Pros:", ln=True)
            self.set_font("Helvetica", "", 9)
            self.set_text_color(51, 51, 51)
            for pro in pros[:2]:
                self.cell(0, 5, f"  + {clean_text(pro)}", ln=True)

        if cons:
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(220, 38, 38)
            self.cell(0, 5, "Cons:", ln=True)
            self.set_font("Helvetica", "", 9)
            self.set_text_color(51, 51, 51)
            for con in cons[:2]:
                self.cell(0, 5, f"  - {clean_text(con)}", ln=True)

        self.ln(8)

def main():
    # 读取工具数据
    data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tools.json")
    with open(data_file, "r", encoding="utf-8") as f:
        tools = json.load(f)

    # 计算评分并排序
    def calculate_total(tool):
        scores = tool.get("scores", {})
        if not scores:
            return 0
        total = 0
        weights = {"functionality": 0.25, "ux": 0.20, "pricing": 0.20, "integration": 0.15, "support": 0.10, "ethics": 0.10}
        for key, weight in weights.items():
            if key in scores and isinstance(scores[key], (int, float)):
                total += scores[key] * weight
        return total

    # 按评分排序，取Top 50
    sorted_tools = sorted(tools, key=calculate_total, reverse=True)[:50]

    # 创建PDF
    pdf = AIToolsPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # 封面
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(26, 86, 219)
    pdf.cell(0, 15, "2026 AI Tools", align="C", ln=True)
    pdf.cell(0, 15, "Selection Guide", align="C", ln=True)
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 10, "Top 50 AI Tools Reviewed & Ranked", align="C", ln=True)
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, "Based on our 6-dimension evaluation methodology:", align="C", ln=True)
    pdf.cell(0, 8, "Functionality (25%) | UX (20%) | Pricing (20%)", align="C", ln=True)
    pdf.cell(0, 8, "Integration (15%) | Support (10%) | Ethics (10%)", align="C", ln=True)
    pdf.ln(30)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, "Generated by AIToolCrux.com", align="C", ln=True)
    pdf.cell(0, 8, "Visit https://www.aitoolcrux.com for more", align="C", ln=True)

    # 目录
    pdf.add_page()
    pdf.chapter_title("Table of Contents")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(51, 51, 51)
    for i, tool in enumerate(sorted_tools[:50], 1):
        pdf.cell(0, 7, f"#{i} {clean_text(tool['name'])} - {clean_text(tool.get('category', 'Unknown'))}", ln=True)

    # 按分类分组
    categories = {}
    for tool in sorted_tools:
        cat = tool.get("category", "Other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(tool)

    # 每个分类的工具
    rank = 1
    for category, category_tools in categories.items():
        pdf.add_page()
        pdf.chapter_title(f"{category.upper()} Tools")
        pdf.ln(5)
        for tool in category_tools:
            if rank > 50:
                break
            # 检查是否需要新页面
            if pdf.get_y() > 250:
                pdf.add_page()
            pdf.tool_card(rank, tool, category)
            rank += 1

    # 结语
    pdf.add_page()
    pdf.chapter_title("Thank You!")
    pdf.chapter_body("Thank you for downloading the 2026 AI Tools Selection Guide. We hope this guide helps you find the perfect AI tools for your needs.")
    pdf.chapter_body("For the latest reviews, comparisons, and updates, visit our website at https://www.aitoolcrux.com")
    pdf.chapter_body("Disclaimer: This guide is for informational purposes only. All tool ratings are based on our independent evaluation methodology and may not reflect the most current features or pricing. Always verify information on the official website before making any decisions.")

    # 保存PDF
    output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public", "ai-tools-guide-2026.pdf")
    pdf.output(output_file)
    print(f"PDF已生成: {output_file}")
    print(f"文件大小: {os.path.getsize(output_file) / 1024:.1f} KB")
    print(f"包含工具数: {len(sorted_tools)}")
    print(f"页数: {pdf.page_no()}")

if __name__ == "__main__":
    main()
