import re

filepath = 'app/ranking/layout.tsx'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换title
old_title = 'Best AI Tools Ranking 2026: Top 533 AI Tools Rated & Compared | AIToolCrux'
new_title = 'Best AI Tools Ranking 2026: Top 533 Rated | AIToolCrux'
content = content.replace(old_title, new_title)

# 替换description
old_desc = 'Discover the definitive ranking of the best AI tools in 2026. 533+ tools evaluated across 6 dimensions with expert reviews, pricing comparison, pros & cons. Find your perfect AI tool.'
new_desc = 'Discover the definitive ranking of the best AI tools in 2026. 533+ tools evaluated across 6 dimensions with expert reviews and pricing comparison.'
content = content.replace(old_desc, new_desc)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Ranking layout updated successfully!")
print(f"  Title: {new_title} ({len(new_title)} chars)")
print(f"  Desc: {new_desc} ({len(new_desc)} chars)")
