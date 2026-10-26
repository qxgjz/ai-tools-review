# AIToolCrux 全站技术SEO审计报告

**生成时间**: 2026-09-17  
**审计工具**: sitemap驱动版（httpx + BeautifulSoup，10并发）  
**数据源**: https://www.aitoolcrux.com/sitemap.xml

## 汇总

| 指标 | 数值 |
|---|---|
| 总URL数 | 905 |
| 有问题的页面 | 473 |
| 总问题数（含重复title/meta/大图/broken link） | 657 |
| P0（影响索引） | 473 |
| P1（影响排名） | 1 |
| P2（小问题） | 0 |
| 大图（>200KB） | 2 |
| broken外链 | 181 |
| 重复Title组 | 1 |
| 重复Meta组 | 0 |

## 问题分类计数

| 问题 | 页面数 |
|---|---|
| 请求失败: The read operation timed out | 434 |
| 请求失败: _ssl.c:1015: The handshake operation timed out | 26 |
| 请求失败: EOF occurred in violation of protocol (_ssl.c:2503) | 9 |
| 请求失败: <StreamReset stream_id:45, error_code:1, remote_reset:True> | 1 |
| 请求失败: <StreamReset stream_id:57, error_code:1, remote_reset:True> | 1 |
| 请求失败: <StreamReset stream_id:47, error_code:1, remote_reset:True> | 1 |
| 请求失败: Server disconnected | 1 |

## P0：影响索引

- https://www.aitoolcrux.com/about/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/privacy/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/generator/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/compare/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/free-ai-tools-guide/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/blog/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/contact/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/ranking/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/disclosure/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/authors/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/chatgpt/ — 请求失败: _ssl.c:1015: The handshake operation timed out
- https://www.aitoolcrux.com/terms/ — 请求失败: _ssl.c:1015: The handshake operation timed out
- https://www.aitoolcrux.com/tools/jasper/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/windsurf/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/cursor/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/copy-ai/ — 请求失败: _ssl.c:1015: The handshake operation timed out
- https://www.aitoolcrux.com/tools/notion-ai/ — 请求失败: _ssl.c:1015: The handshake operation timed out
- https://www.aitoolcrux.com/tools/runway/ — 请求失败: _ssl.c:1015: The handshake operation timed out
- https://www.aitoolcrux.com/tools/grammarly/ — 请求失败: _ssl.c:1015: The handshake operation timed out
- https://www.aitoolcrux.com/tools/suno/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/canva-magic/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/n8n/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/dify/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/auto-gpt/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/perplexity/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/ollama/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/figma-ai/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/llama-cpp/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/sora/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/text-generation-webui/ — 请求失败: <StreamReset stream_id:45, error_code:1, remote_reset:True>
- https://www.aitoolcrux.com/tools/librechat/ — 请求失败: <StreamReset stream_id:57, error_code:1, remote_reset:True>
- https://www.aitoolcrux.com/tools/firecrawl/ — 请求失败: <StreamReset stream_id:47, error_code:1, remote_reset:True>
- https://www.aitoolcrux.com/tools/crawl4ai/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/composio/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/flowise/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/copilotkit/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/openai-python/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/pydantic/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/semantic-kernel/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/llama-factory/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/chroma/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/langgraph/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/openai-translator/ — 请求失败: _ssl.c:1015: The handshake operation timed out
- https://www.aitoolcrux.com/tools/prefect/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/scrapegraph-ai/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/faiss/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/ai/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/repomix/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/dspy/ — 请求失败: The read operation timed out
- https://www.aitoolcrux.com/tools/haystack/ — 请求失败: The read operation timed out
- ... 还有423条

## P1：影响排名

- 重复Title（2页）: "7 Free AI Voice Changers Online 2026 (No Sign-Up)" — https://www.aitoolcrux.com/blog/free-ai-voice-changers-2026/, https://www.aitoolcrux.com/blog/best-free-ai-voice-changers-2026/

## P2：小问题

无 ✅

## 大图（>200KB）

- 283.2KB — https://www.aitoolcrux.com/screenshots/real/webp/planfit-home.webp
- 201.3KB — https://www.aitoolcrux.com/screenshots/real/webp/freeletics-home.webp

## Broken外链（非200）

- ERR:[WinError 10054] 远程主机强迫关闭了一个现有的连接。 — https://github.com/AI-Citizen/SolidGPT
- 403 — https://theresanaiforthat.com
- ERR:[WinError 10054] 远程主机强迫关闭了一个现有的连接。 — https://github.com/eumemic/ai-legion
- 403 — https://ludwig.guru/pricing
- 405 — https://resources.rework.com/tools/ai-agents/best-ai-agents-for-employee-onboarding-2026
- ERR:[WinError 10054] 远程主机强迫关闭了一个现有的连接。 — https://github.com/simonmesmith/agentflow
- ERR:[WinError 10054] 远程主机强迫关闭了一个现有的连接。 — https://github.com/myshell-ai/AIlice
- 404 — https://ahrefs.com/blog/content-optimization-tools/
- ERR:timed out — https://www.heygen.com
- ERR:[WinError 10054] 远程主机强迫关闭了一个现有的连接。 — https://github.com/Stability-AI/generative-models
- ERR:[WinError 10054] 远程主机强迫关闭了一个现有的连接。 — https://github.com/langchain-ai/streamlit-agent
- 405 — https://www.grammarly.com
- ERR:[WinError 10054] 远程主机强迫关闭了一个现有的连接。 — https://github.com/karpathy/autoresearch
- 404 — https://reactagent.io/
- ERR:[WinError 10054] 远程主机强迫关闭了一个现有的连接。 — https://github.com/nilsherzig/LLocalSearch
- ERR:[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] ssl — https://www.nlmatics.com
- ERR:timed out — https://suno.com/pricing
- ERR:timed out — https://github.com/crewAIInc/crewAI-tools
- ERR:timed out — https://writesonic.com/
- 403 — https://www.designhill.com/logo/pricing
- ERR:timed out — https://github.com/KnowledgeCanvas/knowledge
- 403 — https://landbot.io
- ERR:[SSL: CERTIFICATE_VERIFY_FAILED] certifi — https://www.teal.com/pricing
- ERR:timed out — https://leonardo.ai
- 404 — https://www.notion.so/help/notion-ai-for-slack?utm_source=aitoolcrux&utm_medium=affiliate&utm_campaign=review&utm_content=best-ai-slack-bots-2026
- 403 — https://www.notified.com/pricing/
- 403 — https://www.datacamp.com/blog/best-ai-agents
- 403 — https://skylum.com/luminar/pricing
- 403 — https://www.make.com/en/pricing
- ERR:[Errno 11001] getaddrinfo failed — https://play.ht/pricing