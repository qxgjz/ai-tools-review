"""Remove duplicate knowledge entry from knowledge_code.md"""

FILE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\knowledge_code.md"

with open(FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all occurrences of the topic header
topic = "Next.js Image Optimization + Font Optimization (App Router)"
occurrences = []
for i, line in enumerate(lines):
    if topic in line and line.strip().startswith('-'):
        occurrences.append(i)

print(f"Found {len(occurrences)} occurrences at lines: {[o+1 for o in occurrences]}")

if len(occurrences) >= 2:
    # Keep the first one (line index occurrences[0]), remove the second one
    # The second entry starts at occurrences[1], and extends until the next entry or blank line
    start = occurrences[1]
    # Find where this entry ends - look for the next "- [" or "## " line after start
    end = len(lines)
    for j in range(start + 1, len(lines)):
        stripped = lines[j].strip()
        if stripped.startswith('- [') or stripped.startswith('## '):
            end = j
            break
    
    print(f"Removing duplicate lines {start+1} to {end}")
    # Remove the duplicate block
    new_lines = lines[:start] + lines[end:]
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("[OK] Duplicate removed")
else:
    print("[SKIP] No duplicate found")
