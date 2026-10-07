"""
GSC数据分析流水线 - 全自动
调用: python scripts/seo_toolkit/gsc_pipeline.py
输出: iteration_center/gsc_analysis_{日期}.md + 自动写入state.json待办

整合工具:
- Python解析GSC报告
- 3类页面自动识别
- 待办自动写入state.json
"""
import sys, os, json, glob, time, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import *

def find_latest_gsc_report():
    """找最新的GSC报告文件"""
    files = glob.glob(os.path.join(GSC_REPORT_DIR, "*.md"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def parse_gsc_report(filepath):
    """解析GSC报告，提取关键数据"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    data = {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0, "pages": [], "queries": []}

    # 提取总数据
    m = re.search(r'总点击[：:]\s*(\d+)', content)
    if m: data["clicks"] = int(m.group(1))
    m = re.search(r'总曝光[：:]\s*(\d+)', content)
    if m: data["impressions"] = int(m.group(1))
    m = re.search(r'CTR[：:]\s*([\d.]+)%', content)
    if m: data["ctr"] = float(m.group(1))
    m = re.search(r'平均排名[：:]\s*([\d.]+)', content)
    if m: data["position"] = float(m.group(1))

    # 提取页面数据（表格行）
    page_pattern = re.compile(r'(/[^\s|]+)\s*[|]\s*(\d+)\s*[|]\s*(\d+)\s*[|]\s*([\d.]+)%\s*[|]\s*([\d.]+)')
    for m in page_pattern.finditer(content):
        data["pages"].append({
            "page": m.group(1), "clicks": int(m.group(2)),
            "impressions": int(m.group(3)), "ctr": float(m.group(4)),
            "position": float(m.group(5))
        })

    return data

def identify_problem_pages(data):
    """识别3类问题页面"""
    problems = {"high_impression_low_ctr": [], "position_11_20": [], "top3_low_click": []}

    for page in data["pages"]:
        # 高曝光低CTR
        if page["impressions"] > 100 and page["ctr"] < 1.0:
            problems["high_impression_low_ctr"].append(page)
        # 排名11-20
        if 11 <= page["position"] <= 20:
            problems["position_11_20"].append(page)
        # 排名1-3但低点击
        if page["position"] <= 3 and page["ctr"] < 2.0 and page["impressions"] > 20:
            problems["top3_low_click"].append(page)

    return problems

def generate_suggestions(problems):
    """为每个问题页面生成具体优化建议"""
    suggestions = []
    for page in problems["high_impression_low_ctr"]:
        suggestions.append({
            "page": page["page"],
            "type": "CTR优化",
            "priority": "P0",
            "assigned_to": "窗口1",
            "action": f"优化title和meta description。当前曝光{page['impressions']}次CTR仅{page['ctr']}%，排名{page['position']}。新title应含数字+年份+明确利益点，<60字符；meta 150字含CTA。",
            "source": "gsc_pipeline"
        })
    for page in problems["position_11_20"]:
        suggestions.append({
            "page": page["page"],
            "type": "内容优化",
            "priority": "P1",
            "assigned_to": "窗口3",
            "action": f"内容增强以冲入Top10。当前排名{page['position']}，曝光{page['impressions']}。检查：字数是否≥2500、有无对比表、有无FAQ≥5、有无内链≥3、有无Quick Answer。缺什么补什么。",
            "source": "gsc_pipeline"
        })
    for page in problems["top3_low_click"]:
        suggestions.append({
            "page": page["page"],
            "type": "CTR优化（紧急）",
            "priority": "P0",
            "assigned_to": "窗口1",
            "action": f"排名{page['position']}但CTR仅{page['ctr']}%，严重浪费。立即重写title（用数字+情感词+明确承诺），添加FAQPage schema争取Featured Snippet。",
            "source": "gsc_pipeline"
        })
    return suggestions

def write_to_state(suggestions):
    """写入state.json待办"""
    with open(STATE_JSON, "r", encoding="utf-8") as f:
        state = json.load(f)
    existing = {t.get("task","") for t in state.get("next_iteration_focus", [])}
    new_count = 0
    for s in suggestions:
        task_desc = f"[{s['type']}] {s['page']}: {s['action'][:60]}"
        if task_desc not in existing:
            state["next_iteration_focus"].append({
                "id": f"gsc_{s['page'].replace('/','_').replace('?','')}_{int(time.time())}",
                "task": task_desc,
                "assigned_to": s["assigned_to"],
                "priority": s["priority"],
                "source": s["source"],
                "page": s["page"],
                "action": s["action"],
                "status": "pending",
                "created_at": time.strftime("%Y-%m-%d")
            })
            new_count += 1
    with open(STATE_JSON, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    return new_count

def main():
    print(f"=== GSC数据分析流水线 ===")

    # Step 1: 找最新报告
    latest = find_latest_gsc_report()
    if not latest:
        print("[ERROR] 未找到GSC报告文件")
        sys.exit(1)
    print(f"最新报告: {os.path.basename(latest)}")

    # Step 2: 解析
    data = parse_gsc_report(latest)
    print(f"\n总数据: 点击={data['clicks']} 曝光={data['impressions']} CTR={data['ctr']}% 排名={data['position']}")

    # Step 3: 识别问题页面
    problems = identify_problem_pages(data)
    print(f"\n问题页面识别:")
    print(f"  高曝光低CTR: {len(problems['high_impression_low_ctr'])} 个")
    print(f"  排名11-20: {len(problems['position_11_20'])} 个")
    print(f"  Top3低点击: {len(problems['top3_low_click'])} 个")

    # Step 4: 生成建议
    suggestions = generate_suggestions(problems)
    print(f"\n生成优化建议: {len(suggestions)} 条")

    # Step 5: 写入state.json
    new_count = write_to_state(suggestions)
    print(f"新增待办: {new_count} 条")

    # Step 6: 输出报告
    output_file = os.path.join(ITERATION_DIR, f"gsc_analysis_{time.strftime('%Y%m%d')}.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# GSC分析报告 - {time.strftime('%Y-%m-%d')}\n\n")
        f.write(f"## 总数据\n")
        f.write(f"- 点击: {data['clicks']}\n- 曝光: {data['impressions']}\n- CTR: {data['ctr']}%\n- 平均排名: {data['position']}\n\n")
        for ptype, pages in problems.items():
            f.write(f"## {ptype} ({len(pages)}个)\n\n")
            for p in pages:
                f.write(f"- {p['page']}: 曝光={p['impressions']} 点击={p['clicks']} CTR={p['ctr']}% 排名={p['position']}\n")
            f.write("\n")
        f.write(f"## 优化建议（已写入state.json）\n\n")
        for s in suggestions:
            f.write(f"### [{s['priority']}] {s['page']}\n")
            f.write(f"- 类型: {s['type']}\n- 分配: {s['assigned_to']}\n- 行动: {s['action']}\n\n")

    print(f"\n=== 完成 ===")
    print(f"报告: {output_file}")
    print(f"新增待办: {new_count} 条")

if __name__ == "__main__":
    main()
