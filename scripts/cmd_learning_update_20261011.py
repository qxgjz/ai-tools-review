# -*- coding: utf-8 -*-
"""更新 commander_learning.md：关键数据表 + 追加本轮错误与经验"""
import re, datetime

F = r"C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md"
with open(F, encoding="utf-8") as f:
    text = f.read()

# ---------- 1. 更新「网站关键数据」表 ----------
key_rows = {
    "| 文章数 |": "| 文章数 | 154篇 | +48（106→154） |",
    "| 工具数 |": "| 工具数 | 533个 | - |",
    "| 截图数 |": "| 截图数 | 180个 | +62 |",
    "| GSC曝光 |": "| GSC曝光 | 48（新资源10-02~10-06） | 旧资源基线2095 |",
    "| GSC点击 |": "| GSC点击 | 0 | 🔴 |",
    "| GSC CTR |": "| GSC CTR | 0% | 🔴极低 |",
}
lines = text.split("\n")
for i, ln in enumerate(lines):
    for prefix, new in key_rows.items():
        if ln.startswith(prefix):
            lines[i] = new
text = "\n".join(lines)

# ---------- 2. 追加「犯过的错」 ----------
err_row = "| 2026-10-11 | 验证文章URL时直接用打磨师日志中的slug，未先核对 data/posts.json 真实slug → 误判3篇CTR优化为404假完成，浪费多轮验证 | 先查posts.json真实slug，再curl -sL测带尾斜杠URL；308≠404，需跟随重定向 |"

err_marker = None
for m in re.finditer(r"^## .*犯过的错.*$", text, re.M):
    err_marker = m.end()
if err_marker:
    # 找到该章节下的表格最后一行（下一个 ## 或文件尾）
    rest = text[err_marker:]
    next_h = re.search(r"\n## ", rest)
    end = err_marker + (next_h.start() if next_h else len(rest))
    seg = text[err_marker:end]
    if err_row.split("|")[1] not in seg:
        text = text[:end] + err_row + "\n" + text[end:]
        print("已追加犯过的错")
else:
    print("未找到犯过的错章节")

# ---------- 3. 追加「学到的经验」 ----------
exp_row = "| 2026-10-11 | URL验证方法论：①先读data/posts.json拿真实slug ②测带尾斜杠URL ③308后用curl -sL跟随 ④仍404才判假完成——本次3篇CTR优化实际全真完成，教训是验证必须用权威slug源 |"

exp_marker = None
for m in re.finditer(r"^## .*学到的经验.*$", text, re.M):
    exp_marker = m.end()
if exp_marker:
    rest = text[exp_marker:]
    next_h = re.search(r"\n## ", rest)
    end = exp_marker + (next_h.start() if next_h else len(rest))
    seg = text[exp_marker:end]
    if exp_row.split("|")[1] not in seg:
        text = text[:end] + exp_row + "\n" + text[end:]
        print("已追加学到的经验")
else:
    print("未找到学到的经验章节")

with open(F, "w", encoding="utf-8") as f:
    f.write(text)
print("commander_learning.md 更新完成")
