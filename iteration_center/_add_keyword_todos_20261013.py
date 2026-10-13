# -*- coding: utf-8 -*-
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-13"
NOW = datetime.now().isoformat(timespec="seconds")

state_path = os.path.join(BASE, "iteration_center", "state.json")
state = json.load(open(state_path, "r", encoding="utf-8"))

p0_topics = [
    {
        "id": f"KW-{TODAY.replace('-','')}-01",
        "task": "基于关键词 [best ai music generators 2026] 写 2000 字新文章，标题建议 [Best AI Music Generators 2026: Suno vs Udio vs Soundraw Tested]，slug 建议 [/blog/best-ai-music-generators-2026]",
        "assigned_to": ["window2", "创作家"],
        "priority": "P0",
        "status": "pending",
        "source": f"keyword_mining_{TODAY}",
        "keyword": "best ai music generators 2026",
        "serp_competition": "High",
        "serp_verified": True,
        "our_angle": "按用途分类（商用授权/个人创作/视频配乐），附价格和授权模式对比，差异化强调商用授权安全",
        "created_at": NOW,
    },
    {
        "id": f"KW-{TODAY.replace('-','')}-02",
        "task": "基于关键词 [best ai text to speech tools 2026] 写 2000 字新文章，标题建议 [Best AI Text-to-Speech Tools 2026: ElevenLabs vs Murf vs Cartesia]，slug 建议 [/blog/best-ai-text-to-speech-tools-2026]",
        "assigned_to": ["window2", "创作家"],
        "priority": "P0",
        "status": "pending",
        "source": f"keyword_mining_{TODAY}",
        "keyword": "best ai text to speech tools 2026",
        "serp_competition": "High",
        "serp_verified": True,
        "our_angle": "按场景分类（视频配音/客服机器人/播客/开发者API），附每分钟成本和延迟对比，差异化强调开发者友好",
        "created_at": NOW,
    },
    {
        "id": f"KW-{TODAY.replace('-','')}-03",
        "task": "基于关键词 [best ai avatar generators 2026] 写 2000 字新文章，标题建议 [Best AI Avatar Generators 2026: HeyGen vs Synthesia vs D-ID]，slug 建议 [/blog/best-ai-avatar-generators-2026]",
        "assigned_to": ["window2", "创作家"],
        "priority": "P0",
        "status": "pending",
        "source": f"keyword_mining_{TODAY}",
        "keyword": "best ai avatar generators 2026",
        "serp_competition": "High",
        "serp_verified": True,
        "our_angle": "按用户类型分类（企业培训/营销视频/UGC广告/个人品牌），附水印政策和商用权对比，差异化强调无水印方案",
        "created_at": NOW,
    },
]

existing_tasks = [t.get("task", "") for t in state["next_iteration_focus"]]
added = 0
for t in p0_topics:
    if t["task"] in existing_tasks:
        print(f"[SKIP] {t['id']}")
        continue
    state["next_iteration_focus"].append(t)
    added += 1
    print(f"[ADD] {t['id']}: {t['priority']} - {t['keyword']}")

json.dump(state, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\nTotal added: {added}")
print(f"Total todos: {len(state['next_iteration_focus'])}")
