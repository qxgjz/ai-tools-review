import os

screenshot_dir = 'public/screenshots'
os.makedirs(screenshot_dir, exist_ok=True)

def generate_svg(filename, title, subtitle, color1, color2, features):
    """生成美观的SVG界面模拟截图"""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="800" height="500">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color1};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{color2};stop-opacity:1" />
    </linearGradient>
    <linearGradient id="card" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0.95" />
      <stop offset="100%" style="stop-color:#f8fafc;stop-opacity:0.95" />
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="800" height="500" fill="url(#bg)"/>

  <!-- 顶部导航栏 -->
  <rect x="0" y="0" width="800" height="50" fill="#1e293b" opacity="0.9"/>
  <circle cx="25" cy="25" r="8" fill="#ef4444"/>
  <circle cx="45" cy="25" r="8" fill="#f59e0b"/>
  <circle cx="65" cy="25" r="8" fill="#22c55e"/>
  <text x="100" y="30" fill="#94a3b8" font-family="Arial" font-size="12">{title}</text>

  <!-- 侧边栏 -->
  <rect x="0" y="50" width="180" height="450" fill="#0f172a" opacity="0.85"/>
  <text x="20" y="85" fill="#f1f5f9" font-family="Arial" font-size="14" font-weight="bold">{title}</text>
  <text x="20" y="105" fill="#64748b" font-family="Arial" font-size="10">{subtitle}</text>

  <!-- 侧边栏菜单项 -->
  <rect x="10" y="125" width="160" height="30" rx="5" fill="#334155" opacity="0.6"/>
  <text x="25" y="145" fill="#e2e8f0" font-family="Arial" font-size="11">Dashboard</text>

  <rect x="10" y="165" width="160" height="30" rx="5" fill="transparent"/>
  <text x="25" y="185" fill="#94a3b8" font-family="Arial" font-size="11">Projects</text>

  <rect x="10" y="205" width="160" height="30" rx="5" fill="transparent"/>
  <text x="25" y="225" fill="#94a3b8" font-family="Arial" font-size="11">Settings</text>

  <rect x="10" y="245" width="160" height="30" rx="5" fill="transparent"/>
  <text x="25" y="265" fill="#94a3b8" font-family="Arial" font-size="11">Documentation</text>

  <!-- 主内容区 -->
  <rect x="200" y="70" width="580" height="410" rx="10" fill="url(#card)"/>

  <!-- 标题 -->
  <text x="225" y="105" fill="#0f172a" font-family="Arial" font-size="18" font-weight="bold">Welcome to {title}</text>
  <text x="225" y="125" fill="#64748b" font-family="Arial" font-size="11">{subtitle}</text>

  <!-- 统计卡片 -->
  <rect x="225" y="145" width="165" height="70" rx="8" fill="#f1f5f9" stroke="#e2e8f0" stroke-width="1"/>
  <text x="240" y="170" fill="#64748b" font-family="Arial" font-size="10">Total Requests</text>
  <text x="240" y="195" fill="#0f172a" font-family="Arial" font-size="20" font-weight="bold">12,847</text>
  <text x="340" y="195" fill="#22c55e" font-family="Arial" font-size="10">+24%</text>

  <rect x="405" y="145" width="165" height="70" rx="8" fill="#f1f5f9" stroke="#e2e8f0" stroke-width="1"/>
  <text x="420" y="170" fill="#64748b" font-family="Arial" font-size="10">Success Rate</text>
  <text x="420" y="195" fill="#0f172a" font-family="Arial" font-size="20" font-weight="bold">98.7%</text>
  <text x="520" y="195" fill="#22c55e" font-family="Arial" font-size="10">+1.2%</text>

  <rect x="585" y="145" width="175" height="70" rx="8" fill="#f1f5f9" stroke="#e2e8f0" stroke-width="1"/>
  <text x="600" y="170" fill="#64748b" font-family="Arial" font-size="10">Active Users</text>
  <text x="600" y="195" fill="#0f172a" font-family="Arial" font-size="20" font-weight="bold">3,421</text>
  <text x="700" y="195" fill="#22c55e" font-family="Arial" font-size="10">+18%</text>

  <!-- 功能列表 -->
  <text x="225" y="245" fill="#0f172a" font-family="Arial" font-size="14" font-weight="bold">Key Features</text>

  <rect x="225" y="260" width="535" height="1" fill="#e2e8f0"/>

  <!-- 功能项 -->'''

    y_pos = 290
    for i, feature in enumerate(features[:5]):
        svg += f'''
  <circle cx="240" cy="{y_pos}" r="6" fill="{color1}"/>
  <text x="258" y="{y_pos+4}" fill="#334155" font-family="Arial" font-size="12" font-weight="bold">{feature['title']}</text>
  <text x="258" y="{y_pos+20}" fill="#64748b" font-family="Arial" font-size="10">{feature['desc']}</text>'''
        y_pos += 38

    svg += '''

  <!-- 底部活动日志 -->
  <rect x="225" y="450" width="535" height="20" rx="4" fill="#f8fafc"/>
  <circle cx="238" cy="460" r="3" fill="#22c55e"/>
  <text x="250" y="464" fill="#64748b" font-family="Arial" font-size="9">System operational · Last updated: just now</text>
</svg>'''

    filepath = os.path.join(screenshot_dir, f'{filename}.svg')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  Generated: {filename}.svg ({len(svg)} bytes)")

# 为9个缺少截图的工具生成截图
tools_to_generate = [
    {
        'filename': 'ragflow',
        'title': 'RAGFlow',
        'subtitle': 'Deep Document Understanding RAG Engine',
        'color1': '#6366f1',
        'color2': '#8b5cf6',
        'features': [
            {'title': 'Deep Document Parsing', 'desc': 'Layout-aware extraction from PDFs, Word, Excel'},
            {'title': 'Knowledge Base Management', 'desc': 'Organize documents into searchable knowledge bases'},
            {'title': 'Chunking Strategies', 'desc': 'Intelligent text splitting with context preservation'},
            {'title': 'Multi-LLM Support', 'desc': 'Connect to OpenAI, Claude, Gemini, local models'},
            {'title': 'API & Integration', 'desc': 'REST API for seamless application integration'},
        ]
    },
    {
        'filename': 'composio',
        'title': 'Composio',
        'subtitle': 'Agent Tooling Platform',
        'color1': '#0ea5e9',
        'color2': '#06b6d4',
        'features': [
            {'title': '100+ Tool Integrations', 'desc': 'Pre-built connectors for popular apps and APIs'},
            {'title': 'Agent Framework Agnostic', 'desc': 'Works with LangChain, LlamaIndex, AutoGPT, CrewAI'},
            {'title': 'OAuth & Auth Management', 'desc': 'Secure authentication handling for all integrations'},
            {'title': 'Trigger & Actions', 'desc': 'Event-driven automation with webhooks and triggers'},
            {'title': 'Monitoring & Logging', 'desc': 'Track agent tool usage and performance metrics'},
        ]
    },
    {
        'filename': 'librechat',
        'title': 'LibreChat',
        'subtitle': 'Open Source AI Chat Platform',
        'color1': '#10b981',
        'color2': '#14b8a6',
        'features': [
            {'title': 'Multi-LLM Support', 'desc': 'ChatGPT, Claude, Gemini, local models, custom endpoints'},
            {'title': 'Conversation Management', 'desc': 'Organize chats with folders, tags, and search'},
            {'title': 'File & Image Analysis', 'desc': 'Upload documents and images for AI analysis'},
            {'title': 'Plugin System', 'desc': 'Extend functionality with community plugins'},
            {'title': 'User Authentication', 'desc': 'Built-in auth with role-based access control'},
        ]
    },
    {
        'filename': 'auto-gpt',
        'title': 'AutoGPT',
        'subtitle': 'Autonomous AI Agent Platform',
        'color1': '#f59e0b',
        'color2': '#f97316',
        'features': [
            {'title': 'Autonomous Task Execution', 'desc': 'AI agents that plan and execute complex tasks'},
            {'title': 'Memory & Context', 'desc': 'Long-term memory for persistent agent knowledge'},
            {'title': 'Tool & Plugin Ecosystem', 'desc': 'Browse, code, analyze, and more with plugins'},
            {'title': 'Multi-Agent Collaboration', 'desc': 'Coordinate multiple specialized agents for workflows'},
            {'title': 'Monitoring Dashboard', 'desc': 'Track agent progress, logs, and performance'},
        ]
    },
    {
        'filename': 'openai-python',
        'title': 'OpenAI Python',
        'subtitle': 'Official Python SDK',
        'color1': '#10a37f',
        'color2': '#1a7f64',
        'features': [
            {'title': 'Complete API Coverage', 'desc': 'Chat, Completions, Embeddings, Images, Audio, Files'},
            {'title': 'Streaming Support', 'desc': 'Real-time streaming responses with SSE'},
            {'title': 'Type Safety', 'desc': 'Full TypeScript-style type hints with Pydantic models'},
            {'title': 'Async & Sync', 'desc': 'Both synchronous and asynchronous client interfaces'},
            {'title': 'Retry & Error Handling', 'desc': 'Automatic retries with exponential backoff'},
        ]
    },
    {
        'filename': 'litellm',
        'title': 'LiteLLM',
        'subtitle': 'Unified LLM API Gateway',
        'color1': '#8b5cf6',
        'color2': '#a78bfa',
        'features': [
            {'title': '100+ LLM Providers', 'desc': 'OpenAI, Anthropic, Azure, Bedrock, local models'},
            {'title': 'Standardized Interface', 'desc': 'One API call format for all supported providers'},
            {'title': 'Cost Tracking', 'desc': 'Monitor and log token usage and costs per provider'},
            {'title': 'Load Balancing', 'desc': 'Distribute requests across multiple API keys and providers'},
            {'title': 'Fallback & Retry', 'desc': 'Automatic failover when a provider is unavailable'},
        ]
    },
    {
        'filename': 'scrapegraph-ai',
        'title': 'ScrapeGraphAI',
        'subtitle': 'AI Web Scraping Library',
        'color1': '#ec4899',
        'color2': '#f472b6',
        'features': [
            {'title': 'AI-Powered Scraping', 'desc': 'LLM-driven extraction that understands page structure'},
            {'title': 'SmartScraper Graph', 'desc': 'Intelligent extraction with schema validation'},
            {'title': 'SearchGraph', 'desc': 'Multi-page research and information aggregation'},
            {'title': 'ScriptCreator', 'desc': 'Generate reusable Python scraping scripts'},
            {'title': 'Multi-Model Support', 'desc': 'Works with OpenAI, Groq, Ollama, and more'},
        ]
    },
    {
        'filename': 'gpt-researcher',
        'title': 'GPT Researcher',
        'subtitle': 'Autonomous AI Research Agent',
        'color1': '#3b82f6',
        'color2': '#60a5fa',
        'features': [
            {'title': 'Autonomous Research', 'desc': 'AI agent that researches any topic comprehensively'},
            {'title': 'Multi-Source Synthesis', 'desc': 'Aggregates and cross-references 20+ sources'},
            {'title': 'Structured Reports', 'desc': 'Generates detailed, cited research documents'},
            {'title': 'Deep Research Mode', 'desc': 'Extended research with sub-question decomposition'},
            {'title': 'Export & Share', 'desc': 'Export to PDF, Word, Markdown, or share online'},
        ]
    },
    {
        'filename': 'agentscope',
        'title': 'AgentScope',
        'subtitle': 'Multi-Agent Development Platform',
        'color1': '#06b6d4',
        'color2': '#22d3ee',
        'features': [
            {'title': 'Multi-Agent Orchestration', 'desc': 'Build and coordinate complex multi-agent systems'},
            {'title': 'Model Abstraction', 'desc': 'Unified interface for LLMs, multi-modal models'},
            {'title': 'Service Integration', 'desc': 'Built-in tools for search, code, file operations'},
            {'title': 'Workflow Designer', 'desc': 'Visual and programmatic workflow construction'},
            {'title': 'Observability', 'desc': 'Comprehensive logging, tracing, and monitoring'},
        ]
    },
]

print("=== Generating Missing Screenshots ===\n")
for tool in tools_to_generate:
    generate_svg(
        tool['filename'],
        tool['title'],
        tool['subtitle'],
        tool['color1'],
        tool['color2'],
        tool['features']
    )

print(f"\n=== Done! Generated {len(tools_to_generate)} screenshots ===")
print(f"Total screenshots in directory: {len([f for f in os.listdir(screenshot_dir) if f.endswith('.svg')])}")
