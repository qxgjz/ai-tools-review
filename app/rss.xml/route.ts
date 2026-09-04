import { NextResponse } from "next/server";
import postsData from "@/data/posts.json";

export const dynamic = "force-static";

export async function GET() {
  const siteUrl = "https://www.aitoolcrux.com";
  const posts = postsData as any[];

  // 按发布日期排序（最新的在前）
  const sortedPosts = [...posts].sort(
    (a, b) =>
      new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime()
  );

  // 生成RSS XML
  const rssItems = sortedPosts
    .map((post) => {
      const url = `${siteUrl}/blog/${post.slug}`;
      const pubDate = new Date(post.publishedAt).toUTCString();
      const description = post.excerpt
        .replace(/<[^>]*>/g, "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&apos;");
      const title = post.title
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&apos;");
      const author = post.author || "AIToolCrux Editorial Team";

      return `    <item>
      <title>${title}</title>
      <link>${url}</link>
      <guid isPermaLink="true">${url}</guid>
      <pubDate>${pubDate}</pubDate>
      <author>${author}</author>
      <category>${post.category}</category>
      <description>${description}</description>
    </item>`;
    })
    .join("\n");

  const rssContent = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>AIToolCrux - AI Tool Reviews & Comparisons</title>
    <link>${siteUrl}</link>
    <description>Independent AI tool reviews, comparisons, and rankings based on a 6-dimension evaluation methodology. Find the perfect AI tool for your needs.</description>
    <language>en-us</language>
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
    <atom:link href="${siteUrl}/rss.xml" rel="self" type="application/rss+xml" />
    <image>
      <url>${siteUrl}/logo.png</url>
      <title>AIToolCrux - AI Tool Reviews & Comparisons</title>
      <link>${siteUrl}</link>
    </image>
${rssItems}
  </channel>
</rss>`;

  return new NextResponse(rssContent, {
    headers: {
      "Content-Type": "application/rss+xml; charset=utf-8",
      "Cache-Control": "public, max-age=3600, s-maxage=3600",
    },
  });
}
