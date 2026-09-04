"use client";

import { useEffect, useRef } from "react";

/**
 * Giscus 评论系统组件
 * 基于 GitHub Discussions，开源免费，无广告
 *
 * 使用前需要：
 * 1. 在 GitHub 仓库启用 Discussions
 * 2. 安装 Giscus App: https://github.com/apps/giscus
 * 3. 访问 https://giscus.app 获取你的 repoId 和 categoryId
 * 4. 替换下方的配置
 */
interface GiscusProps {
  /** GitHub 仓库，格式：owner/repo */
  repo?: string;
  /** 仓库 ID（从 giscus.app 获取） */
  repoId?: string;
  /** 讨论分类名称 */
  category?: string;
  /** 分类 ID（从 giscus.app 获取） */
  categoryId?: string;
  /** 主题 */
  theme?: "light" | "dark" | "preferred_color_scheme";
  /** 语言 */
  lang?: string;
}

export default function Giscus({
  repo = "qxgjz/ai-tools-review",
  repoId = "R_kgDOULm3Xw",
  category = "Announcements",
  categoryId = "DIC_kwDOULm3X84DEsrT",
  theme = "preferred_color_scheme",
  lang = "en",
}: GiscusProps) {
  const commentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!commentRef.current) return;

    // 清空容器
    commentRef.current.innerHTML = "";

    // 创建 giscus 脚本
    const script = document.createElement("script");
    script.src = "https://giscus.app/client.js";
    script.async = true;
    script.crossOrigin = "anonymous";
    script.setAttribute("data-repo", repo);
    script.setAttribute("data-repo-id", repoId);
    script.setAttribute("data-category", category);
    script.setAttribute("data-category-id", categoryId);
    script.setAttribute("data-mapping", "pathname");
    script.setAttribute("data-strict", "0");
    script.setAttribute("data-reactions-enabled", "1");
    script.setAttribute("data-emit-metadata", "0");
    script.setAttribute("data-input-position", "bottom");
    script.setAttribute("data-theme", theme);
    script.setAttribute("data-lang", lang);
    script.setAttribute("data-loading", "lazy");

    commentRef.current.appendChild(script);
  }, [repo, repoId, category, categoryId, theme, lang]);

  return (
    <div className="mt-12">
      <h2 className="text-xl font-bold text-gray-900 mb-6">Comments & Discussion</h2>
      <div ref={commentRef} className="min-h-[200px]" />
      <p className="text-xs text-gray-400 mt-4">
        Comments powered by Giscus. Sign in with your GitHub account to join the discussion. Comment data is stored in GitHub Discussions.
      </p>
    </div>
  );
}
