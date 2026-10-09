import fs from 'fs';
import path from 'path';

/**
 * 从文章 content 中提取第一张真实截图 URL（服务端专用）
 * 匹配 markdown 图片 ![](url) 或 html <img src="url">
 */
export function getPostCoverImage(content?: string): string | null {
  if (!content) return null;
  const md = content.match(/!\[[^\]]*\]\((\/screenshots\/[^)]+\.webp)\)/);
  if (md) return md[1];
  const html = content.match(/src="(\/screenshots\/[^"]+\.webp)"/);
  return html ? html[1] : null;
}

export function getToolScreenshot(slug: string): string | null {
  try {
    const p = path.join(
      process.cwd(),
      'public',
      'screenshots',
      'real',
      'webp',
      `${slug}.webp`,
    );
    return fs.existsSync(p) ? `/screenshots/real/webp/${slug}.webp` : null;
  } catch {
    return null;
  }
}
