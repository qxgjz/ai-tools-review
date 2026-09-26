import json

with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

print(f'Total articles: {len(posts)}')
print(f'\nLatest 5 articles:')
for i, p in enumerate(posts[:5]):
    title = p.get('title', 'N/A')[:70]
    pub_date = p.get('publishedAt', 'N/A')
    category = p.get('category', 'N/A')
    read_time = p.get('readTime', 'N/A')
    print(f'{i+1}. [{pub_date}] {title}')
    print(f'   Category: {category}, ReadTime: {read_time} min')

# Check if there's an article published today
from datetime import datetime
today = datetime.now().strftime('%Y-%m-%d')
today_articles = [p for p in posts if p.get('publishedAt', '').startswith(today)]
print(f'\nArticles published today ({today}): {len(today_articles)}')
