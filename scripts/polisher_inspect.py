"""Polisher: inspect low-quality articles."""
import json, os
os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

r = json.load(open("iteration_center/zensink_content_quality_report.json", "r", encoding="utf-8"))
print("average_score:", r.get("average_score"))
print("pass_count:", r.get("pass_count"), "fail_count:", r.get("fail_count"))
print()
print("=== low quality articles (sorted asc, top 15) ===")
lq = sorted(r["low_quality_articles"], key=lambda x: x["score"])
for a in lq[:15]:
    print(f'{a["score"]:>3} | wc={a["word_count"]:>4} | {a["slug"]}')
    print(f'     issues: {a["issues"][:4]}')
    print()
