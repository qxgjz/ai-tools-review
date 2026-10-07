import json, os, glob

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

with open("iteration_center/state.json","r",encoding="utf-8") as f:
    state = json.load(f)

nif = state.get("next_iteration_focus", [])
p0_w3 = [t for t in nif if (
    "window3" in str(t.get("assigned_to","")).lower()
    or "窗口3" in str(t.get("assigned_to",""))
) and t.get("priority")=="P0" and t.get("status")=="pending"]

print(f"window3 P0 pending: {len(p0_w3)}")
for i,t in enumerate(p0_w3):
    tid = t.get("id","?")
    task = t.get("task", t.get("title","?"))
    print(f"{i+1}. [{tid}] {task[:100]}")

# Also check P1
p1_w3 = [t for t in nif if (
    "window3" in str(t.get("assigned_to","")).lower()
    or "窗口3" in str(t.get("assigned_to",""))
) and t.get("priority")=="P1" and t.get("status")=="pending"]
print(f"\nwindow3 P1 pending: {len(p1_w3)}")
for i,t in enumerate(p1_w3):
    tid = t.get("id","?")
    task = t.get("task", t.get("title","?"))
    print(f"  P1.{i+1}. [{tid}] {task[:100]}")

# Check GSC reports
gsc_files = sorted(glob.glob("gsc-ga4-report/*.md"), key=os.path.getmtime, reverse=True)
print(f"\nGSC reports available: {len(gsc_files)}")
for f in gsc_files[:3]:
    print(f"  {os.path.basename(f)}")
