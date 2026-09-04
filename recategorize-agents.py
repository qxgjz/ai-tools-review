import json

data = json.load(open('data/tools.json', 'r', encoding='utf-8'))
print(f'原始工具数: {len(data)}')

# 重新分类映射：slug -> 新分类
# 将agent分类中明显属于其他类别的工具重新分类
recategorize_map = {
    # 向量数据库/嵌入数据库 -> database
    'chroma': 'database',
    'weaviate': 'database',
    'qdrant': 'database',
    'milvus': 'database',
    'pinecone': 'database',
    'pgvector': 'database',
    'faiss': 'database',
    'lancedb': 'database',
    'vespa': 'database',
    'typesense': 'database',
    'meilisearch': 'database',

    # LLM推理/运行时/开发工具 -> dev-tools
    'llama-cpp': 'dev-tools',
    'llama-cpp-python': 'dev-tools',
    'vllm': 'dev-tools',
    'ollama': 'dev-tools',
    'text-generation-webui': 'dev-tools',
    'exllama': 'dev-tools',
    'ctransformers': 'dev-tools',
    'ggml': 'dev-tools',
    'mlc-llm': 'dev-tools',
    'lm-studio': 'dev-tools',
    'koboldcpp': 'dev-tools',

    # AI观测/评估/监控 -> observability
    'phoenix': 'observability',
    'deepeval': 'observability',
    'langfuse': 'observability',
    'langsmith': 'observability',
    'helicone': 'observability',
    'promptlayer': 'observability',
    'portkey': 'observability',
    'braintrust': 'observability',
    'agentops': 'observability',

    # 聊天客户端/UI -> chat
    'chatbox': 'chat',
    'chatbot-ui': 'chat',
    'chathub': 'chat',
    'open-webui': 'chat',
    'lobehub': 'chat',
    'chatboxai': 'chat',
    'betterchatgpt': 'chat',
    'chatgpt-next-web': 'chat',
    'librechat': 'chat',

    # 文档处理/OCR/知识库 -> productivity
    'mineru': 'productivity',
    'docling': 'productivity',
    'unstructured': 'productivity',
    'marker': 'productivity',
    'nougat': 'productivity',
    'dify': 'productivity',
    'flowise': 'productivity',
    'langflow': 'productivity',

    # 结构化输出/提示工程 -> code
    'outlines': 'code',
    'instructor': 'code',
    'guidance': 'code',
    'lm-format-enforcer': 'code',
    'jsonformer': 'code',
    'priompt': 'code',
    'gpt-prompt-engineer': 'code',

    # 网页抓取/自动化 -> productivity
    'scrapegraph-ai': 'productivity',
    'firecrawl': 'productivity',
    'browser-use': 'productivity',
    'browsergpt': 'productivity',
    'autogpt-js': 'productivity',
}

# 应用重新分类
recategorized_count = 0
for tool in data:
    slug = tool['slug']
    if slug in recategorize_map:
        old_category = tool['category']
        new_category = recategorize_map[slug]
        if old_category != new_category:
            tool['category'] = new_category
            recategorized_count += 1
            print(f'✅ 重新分类: {tool["name"]} ({slug})')
            print(f'   {old_category} -> {new_category}')

# 保存更新后的数据
json.dump(data, open('data/tools.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print(f'\n═══════════════════════════════════════')
print(f'✅ agent分类优化完成')
print(f'═══════════════════════════════════════')
print(f'重新分类工具数: {recategorized_count}')
print(f'总工具数: {len(data)}')

# 重新统计分类
from collections import Counter
cats = Counter(t.get('category', 'unknown') for t in data)
print(f'\n=== 优化后各分类工具数量 ===')
for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {count}')

# 计算agent分类占比
agent_count = cats.get('agent', 0)
total = len(data)
print(f'\nagent分类占比: {agent_count}/{total} = {agent_count/total*100:.1f}%')
