import { marked } from 'marked';

// 配置marked
marked.setOptions({
  gfm: true, // GitHub Flavored Markdown
  breaks: true, // 换行符转换为<br>
});

/**
 * 将Markdown转换为HTML
 * @param markdown Markdown文本
 * @returns HTML字符串
 */
export function markdownToHtml(markdown: string): string {
  if (!markdown) return '';
  try {
    let html = marked.parse(markdown) as string;
    // Convert h1 to h2: pages already have their own H1, content should not add another
    html = html.replace(/<h1(\s+[^>]*?)>/g, '<h2$1>');
    html = html.replace(/<\/h1>/g, '</h2>');
    // Performance: first image stays eager (LCP element must not be lazy - web.dev top-cwv),
    // later images get lazy. Add explicit dimensions to prevent CLS (all site screenshots are 16:9).
    let imgIndex = 0;
    html = html.replace(/<img(\s+[^>]*?)>/g, (match, attrs) => {
      imgIndex += 1;
      // Add width/height to prevent layout shift when image loads
      let withSize = match;
      if (!/width=/.test(attrs)) {
        withSize = withSize.replace('<img', '<img width="1200" height="675"');
      }
      if (imgIndex === 1) {
        // First image = likely LCP: eager + high priority
        return withSize.replace(/<img/, '<img fetchpriority="high"');
      }
      // Later images: lazy
      return withSize.replace(/<img/, '<img loading="lazy" decoding="async"');
    });
    return html;
  } catch (error) {
    console.error('Markdown conversion error:', error);
    return markdown; // 转换失败时返回原文
  }
}

/**
 * 安全地将Markdown转换为HTML（用于dangerouslySetInnerHTML）
 * @param markdown Markdown文本
 * @returns { __html: string }
 */
export function markdownToHtmlSafe(markdown: string): { __html: string } {
  return { __html: markdownToHtml(markdown) };
}
