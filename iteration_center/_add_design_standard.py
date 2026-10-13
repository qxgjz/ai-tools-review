# -*- coding: utf-8 -*-
"""指挥官：把设计标准值写入state.json.design_standard，窗口7执行时直接读"""
import json
import datetime

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
today = datetime.date.today().isoformat()

d['design_standard'] = {
    "version": "1.0",
    "source": "commander_design_research_20261009 (Linear/Vercel/shadcn/Stripe/thegrain/designkey真实解剖)",
    "colors": {
        "bg_3_layers": ["#ffffff", "#fafafa", "#f4f4f5"],
        "text": ["rgba(0,0,0,0.90)", "rgba(0,0,0,0.60)", "rgba(0,0,0,0.45)"],
        "border": "rgba(0,0,0,0.08)",
        "border_hover": "rgba(0,0,0,0.12)",
        "accent": "#5E6AD2",
        "status": {"done": "#10B981", "progress": "#F59E0B", "cancel": "#EF4444", "todo": "#3B82F6"},
        "forbidden": ["#3b82f6默认蓝作强调色"]
    },
    "typography": {
        "heading_font": "Space Grotesk (备用Inter Display)",
        "heading_letter_spacing": "-0.5~-2.4px",
        "body_font": "Inter 16px",
        "body_line_height": 1.5,
        "display_size": "80-120px",
        "display_line_height": 0.9,
        "weights": ["400", "500", "600"]
    },
    "layout": {
        "grid": "8pt",
        "section_padding": "80-120px",
        "card_gap": "16px或24px",
        "max_width": "1200px",
        "bento_max_cards_per_section": 8,
        "bento_hero": "2×2大卡为视觉起点"
    },
    "radius_shadow": {
        "radius": "8-12px",
        "shadow_as_border": "box-shadow 0 0 0 1px rgba(0,0,0,0.08)",
        "shadow_stack": "边框层+悬浮层+环境光三层"
    },
    "motion": {
        "micro": "100ms",
        "standard": "150ms",
        "page": "250ms",
        "easing": "cubic-bezier(0.16,1,0.3,1)"
    },
    "texture": {
        "noise": "4% SVG噪点 mix-blend-mode:overlay"
    },
    "content_rules": {
        "hero": "真实工具UI截图1.2x放大，禁用抽象插画",
        "title_max_words": 12,
        "logo_wall": "monochrome 40-60%透明度"
    },
    "updated_at": today
}

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('design_standard 已写入 state.json (v1.0)')
print('字段数:', len(d['design_standard']) - 2)
