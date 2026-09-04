"""
将HTML格式的AI工具指南转换为PDF
使用weasyprint库
"""
import os
from weasyprint import HTML, CSS

# 输入输出路径
input_html = "public/ai-tools-guide-2026.html"
output_pdf = "public/2026-ai-tools-guide.pdf"

print(f"正在转换 {input_html} 为 PDF...")

# 自定义CSS，优化PDF显示
custom_css = CSS(string="""
    @page {
        size: A4;
        margin: 2cm;
        @top-center {
            content: "2026 AI Tools Guide - AIToolCrux";
            font-size: 10px;
            color: #666;
        }
        @bottom-center {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 10px;
            color: #666;
        }
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 12px;
        line-height: 1.6;
        color: #333;
    }
    h1 { font-size: 24px; color: #1a56db; page-break-after: avoid; }
    h2 { font-size: 18px; color: #1e40af; page-break-after: avoid; margin-top: 20px; }
    h3 { font-size: 14px; color: #374151; page-break-after: avoid; }
    .tool-card {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
        page-break-inside: avoid;
    }
    .score-bar {
        height: 8px;
        background: #e5e7eb;
        border-radius: 4px;
        overflow: hidden;
    }
    .score-fill {
        height: 100%;
        background: linear-gradient(90deg, #10b981, #3b82f6);
    }
    a { color: #1a56db; text-decoration: none; }
    .toc { page-break-after: always; }
    .toc-item { margin-bottom: 8px; }
""")

try:
    # 生成PDF
    HTML(filename=input_html).write_pdf(
        output_pdf,
        stylesheets=[custom_css]
    )

    # 检查文件大小
    file_size = os.path.getsize(output_pdf)
    file_size_kb = file_size / 1024

    print(f"✅ PDF生成成功: {output_pdf}")
    print(f"   文件大小: {file_size_kb:.1f} KB")

except Exception as e:
    print(f"❌ PDF生成失败: {e}")
    print("提示: weasyprint在Windows上可能需要额外的系统依赖")
    print("备选方案: 用户可以在浏览器中打开HTML文件，使用Ctrl+P保存为PDF")
