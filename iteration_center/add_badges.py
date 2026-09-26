"""Add 3 small badges (no_credit_card, free_quota, hidden_cost) below tool title"""

with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# The existing badge line
old_line = '              {tool.hasFreeTier && <span className="px-2 py-0.5 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 rounded-md text-xs font-semibold">Free Tier Available</span>}'

# New badges to add after it
new_badges = old_line + '''
              {(tool as any).no_credit_card && <span className="px-2 py-0.5 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 rounded-md text-xs font-semibold">No Credit Card</span>}
              {(tool as any).free_quota && <span className="px-2 py-0.5 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-md text-xs font-semibold">Free: {(tool as any).free_quota}</span>}
              {(tool as any).hidden_cost && <span className="px-2 py-0.5 bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400 rounded-md text-xs font-semibold">⚠ {(tool as any).hidden_cost}</span>}'''

if old_line in content:
    content = content.replace(old_line, new_badges)
    print("[OK] Added 3 badges after Free Tier Available")
else:
    print("[ERROR] Could not find the existing badge line")

with open('app/tools/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    verify = f.read()
print(f"  no_credit_card badge present: {'no_credit_card' in verify}")
print(f"  free_quota badge present: {'free_quota' in verify}")
print(f"  hidden_cost badge present: {'hidden_cost' in verify}")
