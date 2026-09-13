import { marked } from "marked";

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
  if (!markdown) return "";
  try {
    return marked.parse(markdown) as string;
  } catch (error) {
    console.error("Markdown conversion error:", error);
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
