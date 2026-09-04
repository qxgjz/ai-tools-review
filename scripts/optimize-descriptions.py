#!/usr/bin/env python3
"""
工具描述优化脚本
自动优化描述过短的工具描述，根据名称、分类、厂商、评分生成更详细的描述
"""

import json
import os

# 分类描述模板
CATEGORY_TEMPLATES = {
    "chat": {
        "prefix": "AI-powered conversational assistant",
        "features": ["natural language understanding", "context-aware responses", "multi-turn dialogue"],
        "use_cases": ["customer support", "content creation", "research assistance", "coding help"],
    },
    "writing": {
        "prefix": "AI-powered writing and content creation tool",
        "features": ["grammar and style correction", "content generation", "tone adjustment", "SEO optimization"],
        "use_cases": ["blog writing", "marketing copy", "email drafting", "social media content"],
    },
    "image": {
        "prefix": "AI-powered image generation and editing tool",
        "features": ["text-to-image generation", "style transfer", "image enhancement", "creative editing"],
        "use_cases": ["digital art", "design prototyping", "marketing visuals", "content creation"],
    },
    "code": {
        "prefix": "AI-powered coding and development assistant",
        "features": ["code completion", "bug detection", "code refactoring", "documentation generation"],
        "use_cases": ["software development", "code review", "learning to code", "debugging"],
    },
    "video": {
        "prefix": "AI-powered video creation and editing tool",
        "features": ["text-to-video generation", "video editing", "auto-captioning", "scene transitions"],
        "use_cases": ["marketing videos", "social media content", "educational content", "creative projects"],
    },
    "audio": {
        "prefix": "AI-powered audio and music generation tool",
        "features": ["text-to-speech", "music generation", "audio enhancement", "voice cloning"],
        "use_cases": ["podcast production", "music creation", "audiobook narration", "sound design"],
    },
    "productivity": {
        "prefix": "AI-powered productivity and workflow automation tool",
        "features": ["task automation", "document processing", "meeting summarization", "workflow optimization"],
        "use_cases": ["office productivity", "project management", "team collaboration", "time management"],
    },
    "search": {
        "prefix": "AI-powered search and research tool",
        "features": ["semantic search", "real-time information", "source citation", "knowledge synthesis"],
        "use_cases": ["academic research", "market analysis", "fact-checking", "learning"],
    },
    "agent": {
        "prefix": "AI-powered autonomous agent platform",
        "features": ["task automation", "multi-step reasoning", "tool integration", "autonomous execution"],
        "use_cases": ["workflow automation", "data processing", "customer service", "complex task execution"],
    },
    "design": {
        "prefix": "AI-powered design and creative tool",
        "features": ["design generation", "layout optimization", "brand consistency", "creative assistance"],
        "use_cases": ["UI/UX design", "marketing materials", "brand identity", "creative projects"],
    },
    "dev-tools": {
        "prefix": "AI-powered developer tool and platform",
        "features": ["code analysis", "deployment automation", "testing assistance", "development workflow"],
        "use_cases": ["software engineering", "DevOps", "code quality", "development productivity"],
    },
    "database": {
        "prefix": "AI-powered database and data management tool",
        "features": ["query optimization", "data analysis", "schema design", "performance tuning"],
        "use_cases": ["data engineering", "analytics", "database management", "business intelligence"],
    },
    "observability": {
        "prefix": "AI-powered monitoring and observability platform",
        "features": ["real-time monitoring", "anomaly detection", "log analysis", "performance tracking"],
        "use_cases": ["application monitoring", "infrastructure management", "incident response", "performance optimization"],
    },
}

# 默认模板
DEFAULT_TEMPLATE = {
    "prefix": "AI-powered tool and platform",
    "features": ["intelligent automation", "smart processing", "advanced capabilities", "user-friendly interface"],
    "use_cases": ["professional work", "creative projects", "business applications", "personal productivity"],
}

def generate_description(tool):
    """根据工具信息生成更详细的描述"""
    name = tool.get("name", "")
    vendor = tool.get("vendor", "")
    category = tool.get("category", "")
    scores = tool.get("scores", {})

    # 获取分类模板
    template = CATEGORY_TEMPLATES.get(category, DEFAULT_TEMPLATE)

    # 计算总分
    total_score = 0
    if scores:
        weights = {"functionality": 0.25, "ux": 0.20, "pricing": 0.20, "integration": 0.15, "support": 0.10, "ethics": 0.10}
        for key, weight in weights.items():
            if key in scores and isinstance(scores[key], (int, float)):
                total_score += scores[key] * weight

    # 构建描述
    parts = []

    # 开头：工具名称 + 类型
    if vendor and vendor.lower() != name.lower():
        parts.append(f"{name} by {vendor} is a {template['prefix']}")
    else:
        parts.append(f"{name} is a {template['prefix']}")

    # 主要功能
    features = template["features"][:2]
    parts.append(f"featuring {features[0]} and {features[1]}")

    # 适用场景
    use_cases = template["use_cases"][:2]
    parts.append(f"designed for {use_cases[0]} and {use_cases[1]}")

    # 评分信息（如果有）
    if total_score > 0:
        grade = ""
        if total_score >= 9:
            grade = "excellent"
        elif total_score >= 8:
            grade = "very good"
        elif total_score >= 7:
            grade = "good"
        elif total_score >= 6:
            grade = "above average"
        else:
            grade = "average"
        parts.append(f"with a {grade} rating of {total_score:.1f}/10 based on our 6-dimension evaluation")

    # 组合描述
    description = ". ".join(parts) + "."

    # 确保描述长度在80-200字符之间
    if len(description) < 80:
        description += f" It offers a comprehensive solution for professionals and businesses looking to leverage AI technology for {use_cases[0]}."

    if len(description) > 250:
        description = description[:247] + "..."

    return description

def main():
    # 读取工具数据
    data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tools.json")
    with open(data_file, "r", encoding="utf-8") as f:
        tools = json.load(f)

    print(f"总工具数: {len(tools)}")

    # 找出描述过短的工具
    short_tools = [t for t in tools if len(t.get("description", "")) < 50]
    print(f"描述过短(<50字符)的工具数: {len(short_tools)}")

    # 优化所有描述过短的工具
    optimized_count = 0
    for tool in tools:
        if len(tool.get("description", "")) < 50:
            old_desc = tool["description"]
            new_desc = generate_description(tool)
            tool["description"] = new_desc
            optimized_count += 1
            if optimized_count <= 5:
                print(f"\n优化 {tool['name']}:")
                print(f"  旧描述 ({len(old_desc)} chars): {old_desc}")
                print(f"  新描述 ({len(new_desc)} chars): {new_desc}")

    print(f"\n已优化 {optimized_count} 个工具的描述")

    # 保存优化后的数据
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)

    print(f"数据已保存到 {data_file}")

    # 验证优化结果
    remaining_short = [t for t in tools if len(t.get("description", "")) < 50]
    print(f"剩余描述过短的工具数: {len(remaining_short)}")

if __name__ == "__main__":
    main()
