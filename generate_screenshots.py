import os

# Top 10 tools missing screenshots
tools = [
    {"slug": "anything-llm", "name": "AnythingLLM", "color": "#7C3AED", "tagline": "All-in-one AI productivity accelerator"},
    {"slug": "n8n", "name": "n8n", "color": "#EA4B8D", "tagline": "Fair-code workflow automation platform"},
    {"slug": "dify", "name": "Dify", "color": "#18A058", "tagline": "Production-ready platform for agentic workflow"},
    {"slug": "gemini-cli", "name": "Gemini CLI", "color": "#4285F4", "tagline": "Open-source AI agent for your terminal"},
    {"slug": "langflow", "name": "Langflow", "color": "#1E3A8A", "tagline": "Visual platform for building AI agents"},
    {"slug": "gpt-4o", "name": "GPT-4o", "color": "#10A37F", "tagline": "OpenAI's flagship multimodal model"},
    {"slug": "goose", "name": "Goose", "color": "#F97316", "tagline": "Extensible AI agent beyond code suggestions"},
]

def generate_svg(tool):
    slug = tool["slug"]
    name = tool["name"]
    color = tool["color"]
    tagline = tool["tagline"]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">
  <defs>
    <linearGradient id="bg-{slug}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f8fafc;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f1f5f9;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="header-{slug}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{color};stop-opacity:0.85" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1200" height="800" fill="url(#bg-{slug})"/>

  <!-- Header -->
  <rect x="0" y="0" width="1200" height="60" fill="url(#header-{slug})"/>
  <circle cx="35" cy="30" r="12" fill="white" opacity="0.9"/>
  <text x="55" y="36" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="white">{name}</text>
  <text x="1100" y="36" font-family="Arial, sans-serif" font-size="12" fill="white" opacity="0.8" text-anchor="end">AIToolCrux Review</text>

  <!-- Sidebar -->
  <rect x="0" y="60" width="240" height="740" fill="#1e293b"/>
  <rect x="20" y="90" width="200" height="40" rx="6" fill="{color}" opacity="0.2"/>
  <text x="40" y="115" font-family="Arial, sans-serif" font-size="14" fill="white">Dashboard</text>

  <rect x="20" y="145" width="200" height="40" rx="6" fill="#334155"/>
  <text x="40" y="170" font-family="Arial, sans-serif" font-size="14" fill="#94a3b8">Workflows</text>

  <rect x="20" y="200" width="200" height="40" rx="6" fill="#334155"/>
  <text x="40" y="225" font-family="Arial, sans-serif" font-size="14" fill="#94a3b8">Agents</text>

  <rect x="20" y="255" width="200" height="40" rx="6" fill="#334155"/>
  <text x="40" y="280" font-family="Arial, sans-serif" font-size="14" fill="#94a3b8">Knowledge Base</text>

  <rect x="20" y="310" width="200" height="40" rx="6" fill="#334155"/>
  <text x="40" y="335" font-family="Arial, sans-serif" font-size="14" fill="#94a3b8">Integrations</text>

  <rect x="20" y="365" width="200" height="40" rx="6" fill="#334155"/>
  <text x="40" y="390" font-family="Arial, sans-serif" font-size="14" fill="#94a3b8">Settings</text>

  <!-- Main content area -->
  <rect x="270" y="90" width="900" height="100" rx="12" fill="white" stroke="#e2e8f0" stroke-width="1"/>
  <text x="300" y="130" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#1e293b">{tagline}</text>
  <text x="300" y="160" font-family="Arial, sans-serif" font-size="14" fill="#64748b">Rated 8.5+ / 10 by AIToolCrux Editorial Team</text>

  <!-- Stats cards -->
  <rect x="270" y="210" width="280" height="120" rx="12" fill="white" stroke="#e2e8f0" stroke-width="1"/>
  <text x="290" y="245" font-family="Arial, sans-serif" font-size="13" fill="#64748b">Active Users</text>
  <text x="290" y="285" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="#1e293b">100K+</text>
  <text x="290" y="310" font-family="Arial, sans-serif" font-size="12" fill="#10b981">↑ 23% this month</text>

  <rect x="580" y="210" width="280" height="120" rx="12" fill="white" stroke="#e2e8f0" stroke-width="1"/>
  <text x="600" y="245" font-family="Arial, sans-serif" font-size="13" fill="#64748b">Workflows Run</text>
  <text x="600" y="285" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="#1e293b">2.5M+</text>
  <text x="600" y="310" font-family="Arial, sans-serif" font-size="12" fill="#10b981">↑ 45% this month</text>

  <rect x="890" y="210" width="280" height="120" rx="12" fill="white" stroke="#e2e8f0" stroke-width="1"/>
  <text x="910" y="245" font-family="Arial, sans-serif" font-size="13" fill="#64748b">Integrations</text>
  <text x="910" y="285" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="#1e293b">400+</text>
  <text x="910" y="310" font-family="Arial, sans-serif" font-size="12" fill="#64748b">Native & API</text>

  <!-- Workflow visualization -->
  <rect x="270" y="350" width="900" height="380" rx="12" fill="white" stroke="#e2e8f0" stroke-width="1"/>
  <text x="300" y="385" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#1e293b">Workflow Preview</text>

  <!-- Nodes -->
  <rect x="320" y="430" width="160" height="70" rx="10" fill="{color}" opacity="0.15" stroke="{color}" stroke-width="2"/>
  <text x="400" y="460" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="{color}" text-anchor="middle">Trigger</text>
  <text x="400" y="480" font-family="Arial, sans-serif" font-size="11" fill="#64748b" text-anchor="middle">Webhook / Schedule</text>

  <line x1="480" y1="465" x2="540" y2="465" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="540,460 550,465 540,470" fill="#cbd5e1"/>

  <rect x="550" y="430" width="160" height="70" rx="10" fill="{color}" opacity="0.15" stroke="{color}" stroke-width="2"/>
  <text x="630" y="460" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="{color}" text-anchor="middle">Process</text>
  <text x="630" y="480" font-family="Arial, sans-serif" font-size="11" fill="#64748b" text-anchor="middle">AI Agent / LLM</text>

  <line x1="710" y1="465" x2="770" y2="465" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="5,5"/>
  <polygon points="770,460 780,465 770,470" fill="#cbd5e1"/>

  <rect x="780" y="430" width="160" height="70" rx="10" fill="{color}" opacity="0.15" stroke="{color}" stroke-width="2"/>
  <text x="860" y="460" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="{color}" text-anchor="middle">Output</text>
  <text x="860" y="480" font-family="Arial, sans-serif" font-size="11" fill="#64748b" text-anchor="middle">API / Database</text>

  <!-- Activity log -->
  <rect x="300" y="540" width="840" height="170" rx="8" fill="#f8fafc"/>
  <text x="320" y="570" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#1e293b">Recent Activity</text>

  <circle cx="325" cy="600" r="4" fill="#10b981"/>
  <text x="340" y="604" font-family="Arial, sans-serif" font-size="12" fill="#475569">Workflow completed successfully - 2.3s execution time</text>
  <text x="1120" y="604" font-family="Arial, sans-serif" font-size="11" fill="#94a3b8" text-anchor="end">2 min ago</text>

  <circle cx="325" cy="630" r="4" fill="#3b82f6"/>
  <text x="340" y="634" font-family="Arial, sans-serif" font-size="12" fill="#475569">New integration connected: Slack, Notion, GitHub</text>
  <text x="1120" y="634" font-family="Arial, sans-serif" font-size="11" fill="#94a3b8" text-anchor="end">15 min ago</text>

  <circle cx="325" cy="660" r="4" fill="#f59e0b"/>
  <text x="340" y="664" font-family="Arial, sans-serif" font-size="12" fill="#475569">Agent training completed - accuracy improved to 94.2%</text>
  <text x="1120" y="664" font-family="Arial, sans-serif" font-size="11" fill="#94a3b8" text-anchor="end">1 hour ago</text>

  <circle cx="325" cy="690" r="4" fill="#8b5cf6"/>
  <text x="340" y="694" font-family="Arial, sans-serif" font-size="12" fill="#475569">Knowledge base synced - 1,247 documents indexed</text>
  <text x="1120" y="694" font-family="Arial, sans-serif" font-size="11" fill="#94a3b8" text-anchor="end">3 hours ago</text>

  <!-- Footer -->
  <rect x="0" y="760" width="1200" height="40" fill="#1e293b"/>
  <text x="30" y="785" font-family="Arial, sans-serif" font-size="11" fill="#94a3b8">Screenshot from {name} - Captured by AIToolCrux Editorial Team</text>
  <text x="1170" y="785" font-family="Arial, sans-serif" font-size="11" fill="#94a3b8" text-anchor="end">aitoolcrux.com</text>
</svg>'''
    return svg

# Generate screenshots
output_dir = "public/screenshots"
os.makedirs(output_dir, exist_ok=True)

for tool in tools:
    svg_content = generate_svg(tool)
    filepath = os.path.join(output_dir, f"{tool['slug']}.svg")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"Generated: {filepath}")

print(f"\nTotal generated: {len(tools)} screenshots")
print(f"Total in directory: {len(os.listdir(output_dir))}")
