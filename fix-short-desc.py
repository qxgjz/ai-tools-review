import json

data = json.load(open('data/tools.json', 'r', encoding='utf-8'))

# 为描述过短的工具补充详细描述
# 基于工具名称、类别和已知信息生成合理描述
description_fixes = {
    'llama-cpp': 'llama.cpp is a high-performance LLM inference engine written in C/C++, enabling efficient local deployment of large language models on consumer hardware with support for multiple quantization formats.',
    'flowise': 'Flowise is a low-code visual platform for building customized LLM flows and AI agents, featuring drag-and-drop interface, integration with major LLM providers, and seamless deployment capabilities.',
    'chroma': 'Chroma is an open-source embedding database designed for AI applications, providing fast and scalable vector storage with built-in embedding functions, ideal for RAG pipelines and semantic search.',
    'scrapegraph-ai': 'ScrapeGraphAI is a Python web scraping library that leverages LLMs and graph logic to automatically extract structured data from websites, supporting both single-page and multi-page scraping workflows.',
    'chatbox': 'Chatbox is a powerful cross-platform AI client desktop application that supports multiple LLM providers including OpenAI, Claude, and local models, featuring prompt management, conversation history, and API cost tracking.',
    'temporal': 'Temporal is a durable execution platform for building reliable distributed applications and microservices, providing workflow orchestration, automatic retries, and state management for complex business logic.',
    'llama-cpp-python': 'llama-cpp-python provides Python bindings for llama.cpp, enabling high-performance LLM inference in Python with support for OpenAI-compatible API server, LangChain integration, and multiple hardware acceleration backends.',
    'outlines': 'Outlines is a text generation library that provides structured outputs for LLMs, enabling reliable JSON, regex, and type-constrained generation with support for major model providers and efficient sampling algorithms.',
    'phoenix': 'Phoenix is an open-source AI observability and evaluation platform by Arize AI, providing LLM tracing, prompt engineering tools, evaluation datasets, and visualization for debugging and improving AI applications in production.',
    'deepeval': 'DeepEval is an open-source LLM evaluation framework that enables unit testing for LLMs and RAG pipelines, featuring 14+ evaluation metrics, synthetic test data generation, and CI/CD integration for continuous quality assurance.',
    'instructor': 'Instructor is a Python library for structured outputs from LLMs, providing reliable JSON extraction with Pydantic validation, retry logic, and support for OpenAI, Anthropic, and other major model providers.',
    'grok-1': 'Grok-1 is an open-source large language model released by xAI, featuring a 314 billion parameter Mixture-of-Experts architecture with 86 billion active parameters, designed for advanced reasoning and knowledge tasks.',
    'babyagi': 'BabyAGI is an open-source AI agent framework that demonstrates task-driven autonomous behavior, using LLMs to create, prioritize, and execute tasks iteratively, serving as a foundational example for AI agent development.',
    'gpt-pilot': 'GPT Pilot is an AI developer tool that acts as the first real AI developer, capable of building entire applications from scratch by breaking down requirements, writing code, running tests, and debugging iteratively.',
    'chatbot-ui': 'Chatbot UI is an open-source AI chat interface for any LLM model, providing a clean and customizable user experience with support for multiple providers, conversation management, prompt templates, and plugin integration.',
    'chat-langchain': 'Chat LangChain is an open-source conversational AI application built with LangChain, demonstrating RAG (Retrieval-Augmented Generation) capabilities with document ingestion, semantic search, and contextual chat responses.',
    'chathub': 'ChatHub is an all-in-one AI chatbot client that enables simultaneous conversations with multiple LLMs including ChatGPT, Claude, Gemini, and more, featuring side-by-side comparison, prompt library, and markdown support.',
    'gpt-prompt-engineer': 'GPT Prompt Engineer is an open-source tool that automatically generates, tests, and optimizes prompts for LLMs, using AI to create multiple prompt variations and evaluate their performance to find the most effective prompts.',
    'openchatkit': 'OpenChatKit is an open-source toolkit for building specialized and general-purpose chatbots, providing a 20 billion parameter model, customization recipes, and evaluation tools for creating production-ready conversational AI.',
    'mistral-finetune': 'Mistral Finetune is an open-source library for fine-tuning Mistral AI models, providing efficient training pipelines with LoRA, QLoRA, and full fine-tuning support, along with data preparation and evaluation tools.',
    'core': 'Cheshire Cat Core is an open-source AI agent microservice framework that enables building custom AI assistants with long-term memory, tool usage, and plugin extensibility, designed for self-hosted and privacy-focused deployments.',
    'priompt': 'Priompt is a JSX-based prompt design library that enables building LLM prompts with conditional rendering, priority-based token allocation, and reusable components, making complex prompt engineering more maintainable and efficient.',
    'second-brain-agent': 'Second Brain AI Agent is an open-source personal knowledge management agent that helps organize, connect, and retrieve information using AI, featuring note-taking, semantic search, and automated knowledge graph building.',
    'dev-gpt': 'Dev-GPT by Jina AI is a virtual development team platform that uses AI agents to handle software development tasks, including code generation, testing, documentation, and deployment, enabling teams to build faster with AI assistance.',
    'dialoqbase': 'Dialoqbase is an open-source platform for creating AI chatbots with ease, featuring RAG capabilities, document ingestion, multiple LLM provider support, and a user-friendly interface for building and deploying conversational AI applications.',
    'loopgpt': 'LoopGPT is a modular Auto-GPT framework that provides a reusable and extensible architecture for building autonomous AI agents, featuring pluggable modules for memory, tools, and reasoning, with support for both Python and CLI interfaces.',
    'evo-ninja': 'Evo.ninja is a versatile generalist AI agent designed for complex task execution, featuring tool integration, multi-step reasoning, and adaptive problem-solving capabilities across various domains including coding, research, and automation.',
    'browsergpt': 'BrowserGPT is an open-source browser automation tool that enables commanding your web browser with natural language using GPT, allowing users to automate repetitive tasks, extract data, and navigate websites through conversational instructions.',
    'autogpt-js': 'AutoGPT.js is a JavaScript implementation of Auto-GPT that runs in the browser, enabling autonomous AI agent capabilities without backend infrastructure, featuring task decomposition, tool usage, and iterative execution in a client-side environment.',
    'agentforge': 'AgentForge is an extensible AGI framework for building custom AI agents, providing a modular architecture with support for multiple LLM providers, memory systems, tool integration, and hierarchical agent orchestration for complex workflows.',
    'automata': 'Automata is a self-coding AI agent that can write, test, and modify its own codebase, featuring advanced code understanding, repository navigation, and autonomous software development capabilities for building and maintaining complex software projects.',
    'yeagerai-agent': 'YeagerAI Agent is an open-source AI agent framework that enables building autonomous agents with tool usage, memory, and reasoning capabilities, designed for developers to create custom AI assistants and automation workflows.',
    'snowchat': 'SnowChat is an open-source text-to-SQL chatbot for Snowflake, enabling users to query their data warehouse using natural language, featuring schema understanding, SQL generation, query execution, and result visualization for data analysts.',
    'prompt2ui': 'Prompt2UI is an experimental tool that generates UI components from natural language prompts, enabling rapid prototyping of user interfaces by describing desired functionality and layout in conversational text.',
    'npi': 'NPI (Neural Plugin Interface) is an action library for AI agents that provides a standardized interface for tool usage, enabling agents to interact with external systems, APIs, and applications through a unified and extensible action framework.',
}

# 更新描述
updated_count = 0
for tool in data:
    slug = tool['slug']
    if slug in description_fixes:
        old_desc = tool.get('description', '')
        if len(old_desc) < 30:
            tool['description'] = description_fixes[slug]
            updated_count += 1
            print(f'✅ 已更新: {tool["name"]} ({slug})')
            print(f'   旧: "{old_desc}"')
            print(f'   新: "{description_fixes[slug][:80]}..."')
            print()

# 保存更新后的数据
json.dump(data, open('data/tools.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print(f'═══════════════════════════════════════')
print(f'✅ 描述补充完成')
print(f'═══════════════════════════════════════')
print(f'已更新工具数: {updated_count}')
print(f'总工具数: {len(data)}')

# 重新检查描述过短的工具
remaining_short = [t for t in data if len(t.get('description', '')) < 30]
print(f'剩余描述过短工具数: {len(remaining_short)}')
if remaining_short:
    print('剩余工具:')
    for t in remaining_short:
        print(f'  - {t["name"]} ({t["slug"]}): "{t["description"]}"')
