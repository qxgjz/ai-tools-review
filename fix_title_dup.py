with open('app/layout.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''  title: {
    default: "Best AI Tools 2026: Expert Reviews & Comparisons | AIToolCrux",
    template: "%s | AIToolCrux",
  },'''

new = '  title: "Best AI Tools 2026: Expert Reviews & Comparisons | AIToolCrux",'

if old in content:
    content = content.replace(old, new)
    with open('app/layout.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed: removed title template to avoid duplicate brand name')
else:
    print('Pattern not found, checking current state...')
    if 'template: "%s | AIToolCrux"' in content:
        print('Template still exists but pattern mismatch')
    else:
        print('Template already removed')
