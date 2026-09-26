"""Append learning-driven focus items to state.json next_iteration_focus."""
import json

path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json"
with open(path, "r", encoding="utf-8") as f:
    state = json.load(f)

new_items = [
    {
        "id": "GHACT-CACHE-002",
        "source": "learning: GitHub Actions caching 2026-09-20",
        "title": "Add dependency + build caching to GitHub Actions workflows",
        "how_to": "For any Next.js build workflow: use actions/setup-node@v4 with cache:'npm', and actions/cache@v4 to cache .next/cache with key containing package-lock.json hash + source file hashes. For python workflows (gsc-fetch, context-update, uptime-monitor): cache ~/.cache/pip. Never cache node_modules directly.",
        "priority": "P2"
    },
    {
        "id": "GHACT-CACHE-003",
        "source": "learning: GitHub Actions caching 2026-09-20",
        "title": "Use setup-node cache:'npm' instead of manual actions/cache for deps",
        "how_to": "In new workflows, prefer actions/setup-node with cache:'npm' (auto-handles ~/.npm). Only use manual actions/cache for .next/cache build output. restore-keys with prefix for partial fallback.",
        "priority": "P2"
    },
]

existing = {item.get("id") if isinstance(item, dict) else None for item in state.get("next_iteration_focus", [])}
added = 0
for item in new_items:
    if item["id"] not in existing:
        state["next_iteration_focus"].append(item)
        added += 1

with open(path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"Added {added} new focus items. Total: {len(state['next_iteration_focus'])}")
