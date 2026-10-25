# -*- coding: utf-8 -*-
import io,os
p=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\window_logs\polisher_2026-10-25.md'
block="""

## R33 SOP轮（2026-10-25 晚）
### CTR重写7篇（title50-59 / meta122-133，数字+年份+情绪+CTA）
| 页面 | t | e |
|---|---|---|
| dify_ai_review | 50 | 133 |
| stable-diffusion-review-2026 | 55 | 123 |
| cursor_ai_review | 59 | 129 |
| gemini_38_flash_review | 54 | 122 |
| openai_astra_review | 57 | 126 |
| creatium-coach-review-2025 | 56 | 125 |
| midjourney-v7-review-2026 | 56 | 130 |

### 低分达标
| slug | zens | Flesch |
|---|---|---|
| heygen-vs-veed-2026 | 88 | 51.0 |
| grammarly-vs-prowritingaid-2026 | 88 | 50.3 |
| veed-vs-capcut-2026 | 88 | 55.7 |
| claude-code-vs-copilot-2026 | 88 | 51.1 |
（deepl-vs-google-translate zens88 Flesch48.2差1.8，待短句打磨）
"""
with io.open(p,'a',encoding='utf-8',newline='') as f: f.write(block)
print('log ok')
