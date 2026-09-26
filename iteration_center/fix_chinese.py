"""Fix Chinese text in generator.ts and generator/page.tsx"""

# Fix 1: lib/generator.ts - generateReason function
with open('lib/generator.ts', 'r', encoding='utf-8') as f:
    content = f.read()

old_reason = '''  const parts: string[] = [];
  parts.push(`${tool.name} 综合评分 ${total.toFixed(1)} 分`);
  if (matchedDims.length > 0) {
    const dimNames = matchedDims.map((d) => DIMENSION_LABELS[d]).join("、");
    parts.push(`在${dimNames}方面表现突出`);
  }
  if (tool.hasFreeTier) parts.push("Free version available to try");
  parts.push(`适合${SCENARIO_LABELS[scenario] || "General"}场景使用`);
  return parts.join("，") + "。";'''

new_reason = '''  const parts: string[] = [];
  parts.push(`${tool.name} overall score ${total.toFixed(1)}/10`);
  if (matchedDims.length > 0) {
    const dimNames = matchedDims.map((d) => DIMENSION_LABELS[d]).join(", ");
    parts.push(`stands out in ${dimNames}`);
  }
  if (tool.hasFreeTier) parts.push("Free version available to try");
  parts.push(`best suited for ${SCENARIO_LABELS[scenario] || "General"} use cases`);
  return parts.join(". ") + ".";'''

if old_reason in content:
    content = content.replace(old_reason, new_reason)
    print("[OK] Fixed generator.ts generateReason()")
else:
    print("[SKIP] generateReason pattern not found")

with open('lib/generator.ts', 'w', encoding='utf-8') as f:
    f.write(content)

# Fix 2: app/generator/page.tsx - Chinese comma joins
with open('app/generator/page.tsx', 'r', encoding='utf-8') as f:
    content2 = f.read()

# Line 52: .join("、")
old1 = '.join("、")'
new1 = '.join(", ")'
count = content2.count(old1)
if count > 0:
    content2 = content2.replace(old1, new1)
    print(f"[OK] Fixed {count} Chinese comma joins in generator/page.tsx")
else:
    print("[SKIP] No Chinese commas found in generator/page.tsx")

with open('app/generator/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content2)

# Verify no Chinese characters remain in rendered strings
import re
for fname in ['lib/generator.ts', 'app/generator/page.tsx']:
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    # Find Chinese chars not in comments
    lines = c.split('\n')
    rendered_chinese = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('/*'):
            continue
        if re.search(r'[\u4e00-\u9fff]', line):
            rendered_chinese.append(f"  Line {i}: {line.strip()[:80]}")
    if rendered_chinese:
        print(f"\n[WARNING] Chinese remaining in {fname}:")
        for rc in rendered_chinese:
            print(rc)
    else:
        print(f"[CLEAN] No rendered Chinese in {fname}")
