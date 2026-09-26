path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\blog\tag\[slug]\page.tsx"

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 在 generateMetadata 之前插入 force-static + generateStaticParams
insert_code = '''export const dynamic = "force-static";
export const dynamicParams = false;

export function generateStaticParams() {
  const tagSlugs = new Set<string>();
  posts.forEach((post: any) => {
    (post.tags || []).forEach((tag: string) => {
      tagSlugs.add(tag.toLowerCase().trim().replace(/[^a-z0-9\\s-]/g, '').replace(/\\s+/g, '-').replace(/-+/g, '-'));
    });
  });
  return Array.from(tagSlugs).map((slug) => ({ slug }));
}

'''

content = content.replace(
    'export function generateMetadata({ params }: TagPageProps)',
    insert_code + 'export function generateMetadata({ params }: TagPageProps)'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
