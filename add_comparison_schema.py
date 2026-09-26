import re

# 1. 在Schema.tsx中添加ComparisonSchema组件
schema_file = 'components/seo/Schema.tsx'

with open(schema_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 添加ComparisonSchema组件（在WebSiteSchema之后）
comparison_schema = '''

interface ComparisonItem {
  name: string;
  description?: string;
  ratingValue?: number;
  price?: string;
  url?: string;
  pros?: string[];
  cons?: string[];
}

interface ComparisonSchemaProps {
  name: string;
  description: string;
  items: ComparisonItem[];
  author?: string;
  datePublished?: string;
}

/**
 * Comparison Schema - 产品对比结构化数据
 * 帮助Search引擎理解对比文章，显示对比富摘要
 */
export function ComparisonSchema({
  name,
  description,
  items,
  author = "AIToolCrux Editorial Team",
  datePublished = new Date().toISOString().split("T")[0],
}: ComparisonSchemaProps) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": name,
    "description": description,
    "author": {
      "@type": "Organization",
      "name": author,
    },
    "datePublished": datePublished,
    "publisher": {
      "@type": "Organization",
      "name": "AIToolCrux",
      "url": "https://www.aitoolcrux.com",
    },
    "about": items.map((item) => ({
      "@type": "SoftwareApplication",
      "name": item.name,
      "description": item.description || "",
      "applicationCategory": "AI Tool",
      "operatingSystem": "Web",
      ...(item.ratingValue && {
        "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": item.ratingValue,
          "bestRating": "10",
          "worstRating": "1",
          "ratingCount": "1",
        },
      }),
      ...(item.price && {
        "offers": {
          "@type": "Offer",
          "price": item.price === "Free" ? "0" : item.price,
          "priceCurrency": "USD",
        },
      }),
      ...(item.url && { "url": item.url }),
    })),
    "mainEntity": {
      "@type": "ItemList",
      "itemListElement": items.map((item, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "item": {
          "@type": "SoftwareApplication",
          "name": item.name,
          ...(item.ratingValue && {
            "aggregateRating": {
              "@type": "AggregateRating",
              "ratingValue": item.ratingValue,
              "bestRating": "10",
              "ratingCount": "1",
            },
          }),
        },
      })),
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
'''

# 在文件末尾添加ComparisonSchema
content += comparison_schema

with open(schema_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Added ComparisonSchema component to Schema.tsx")

# 2. 在文章详情页中导入并使用ComparisonSchema（对于对比类文章）
article_page = 'app/blog/[slug]/page.tsx'

with open(article_page, 'r', encoding='utf-8') as f:
    article_content = f.read()

# 添加ComparisonSchema导入
old_import = 'import { BreadcrumbSchema, ProductSchema, FAQSchema } from "@/components/seo/Schema";'
new_import = 'import { BreadcrumbSchema, ProductSchema, FAQSchema, ComparisonSchema } from "@/components/seo/Schema";'

if old_import in article_content:
    article_content = article_content.replace(old_import, new_import)
    print("✓ Added ComparisonSchema import to article page")
else:
    # 尝试查找其他导入模式
    import_match = re.search(r'import.*Schema.*from.*@/components/seo/Schema.*', article_content)
    if import_match:
        old_import_line = import_match.group(0)
        if 'ComparisonSchema' not in old_import_line:
            new_import_line = old_import_line.replace('}', ', ComparisonSchema }')
            article_content = article_content.replace(old_import_line, new_import_line)
            print("✓ Added ComparisonSchema import to article page (alternative pattern)")

# 在文章详情页中添加ComparisonSchema使用（对于包含"vs"或"comparison"的文章）
# 找到FAQSchema使用的位置，在其后添加ComparisonSchema
old_faq_usage = '{post.faqs && post.faqs.length > 0 && <FAQSchema faqs={post.faqs} />}'
new_faq_usage = '''{post.faqs && post.faqs.length > 0 && <FAQSchema faqs={post.faqs} />}
      {/* Comparison Schema for comparison articles */}
      {(post.title.toLowerCase().includes(" vs ") || post.title.toLowerCase().includes("comparison") || post.category?.toLowerCase().includes("comparison")) && tool && (
        <ComparisonSchema
          name={post.title}
          description={post.excerpt || post.description || `Comprehensive comparison of AI tools by AIToolCrux.`}
          items={[
            {
              name: toolName,
              description: tool.description,
              ratingValue: avgScore,
              price: tool.pricing?.[0]?.price || "Free",
              url: `https://www.aitoolcrux.com/tools/${tool.slug}`,
            },
            ...relatedTools.slice(0, 2).map((rt: any) => ({
              name: rt.name,
              description: rt.description,
              ratingValue: rt.scores ? Object.values(rt.scores).reduce((a: number, b: any) => a + (typeof b === "number" ? b : 0), 0) / Object.keys(rt.scores || {}).length : 7.5,
              price: rt.pricing?.[0]?.price || "Free",
              url: `https://www.aitoolcrux.com/tools/${rt.slug}`,
            })),
          ]}
        />
      )}'''

if old_faq_usage in article_content:
    article_content = article_content.replace(old_faq_usage, new_faq_usage)
    print("✓ Added ComparisonSchema usage to article page")
else:
    print("⚠️ Could not find FAQSchema usage pattern, trying alternative...")
    # 尝试查找其他模式
    faq_match = re.search(r'\{post\.faqs.*FAQSchema.*\}', article_content)
    if faq_match:
        print(f"  Found alternative pattern: {faq_match.group(0)[:80]}")

with open(article_page, 'w', encoding='utf-8') as f:
    f.write(article_content)

print("\n=== Comparison Schema Addition Complete ===")
print("  - Added ComparisonSchema component")
print("  - Added import to article page")
print("  - Added usage for comparison articles (vs/comparison)")
print("  - Comparison schema includes: Article + ItemList + SoftwareApplication + AggregateRating")
