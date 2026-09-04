import json
import re

with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

# 子分类关键词映射
CATEGORY_KEYWORDS = {
    'agent-framework': [
        'framework', 'orchestrat', 'crew', 'langchain', 'langgraph', 'agno',
        'semantic-kernel', 'haystack', 'mastra', 'fabric', 'autogen', 'crewai',
        'agentic', 'multi-agent', 'role-playing', 'autonomous agent',
        'agent engineering', 'build agent', 'agent framework',
    ],
    'agent-runtime': [
        'runtime', 'platform', 'openhands', 'goose', 'cli', 'terminal',
        'code agent', 'coding agent', 'devin', 'ai-driven development',
        'agentic coding', 'lives in your', 'desktop agent',
    ],
    'memory': [
        'memory', 'mem0', 'letta', 'zep', 'recall', 'universal memory',
        'memory layer', 'long-term memory', 'knowledge base',
    ],
    'rag': [
        'rag', 'retrieval', 'llamaindex', 'ragflow', 'privategpt',
        'document agent', 'retrieval-augmented', 'vector search',
        'ocr platform', 'context engine',
    ],
    'dev-tools': [
        'sdk', 'library', 'api', 'python', 'typescript', 'javascript',
        'pydantic', 'copilotkit', 'toolkit', 'frontend stack',
        'generative ui', 'official python', 'official sdk',
        'model context protocol', 'mcp', 'data validation',
    ],
}

def classify_tool(tool):
    """根据工具名称和描述分类到子分类"""
    name = tool.get('name', '').lower()
    desc = tool.get('description', '').lower()
    text = f"{name} {desc}"

    # 计算每个分类的匹配分数
    scores = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in text:
                score += 1
        if score > 0:
            scores[cat] = score

    if scores:
        # 返回分数最高的分类
        return max(scores, key=scores.get)
    return None

# 统计重新分类结果
reclassified = {}
agent_count = 0

for tool in tools:
    if tool.get('category') != 'agent':
        continue

    agent_count += 1
    new_cat = classify_tool(tool)

    if new_cat:
        reclassified[new_cat] = reclassified.get(new_cat, 0) + 1
        tool['category'] = new_cat
    # 否则保持agent分类

print(f'原始agent分类工具数: {agent_count}')
print(f'\n重新分类结果:')
for cat, count in sorted(reclassified.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {count}')

remaining_agent = agent_count - sum(reclassified.values())
print(f'  保持agent分类: {remaining_agent}')

# 保存更新后的tools.json
with open('data/tools.json', 'w', encoding='utf-8') as f:
    json.dump(tools, f, ensure_ascii=False, indent=2)

print(f'\n✅ 已保存更新后的tools.json')

# 统计最终分类
final_cats = {}
for tool in tools:
    cat = tool.get('category', 'unknown')
    final_cats[cat] = final_cats.get(cat, 0) + 1

print(f'\n最终分类统计:')
for cat, count in sorted(final_cats.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {count}')
