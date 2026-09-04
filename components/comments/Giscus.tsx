"use client";

import { useEffect, useRef } from "react";

/**
 * Giscus Comment System Component
 * Based on GitHub Discussions, open source, free, no ads
 *
 * Before using:
 * 1. Enable Discussions in your GitHub repository
 * 2. Install Giscus App: https://github.com/apps/giscus
 * 3. Visit https://giscus.app to get your repoId and categoryId
 * 4. Replace the configuration below
 */
interface GiscusProps {
  /** GitHub repository, format: owner/repo */
  repo?: string;
  /** Repository ID (obtained from giscus.app) */
  repoId?: string;
  /** Discussion category name */
  category?: string;
  /** Category ID (obtained from giscus.app) */
  categoryId?: string;
  /** Theme */
  theme?: "light" | "dark" | "preferred_color_scheme";
  /** Language */
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

    // Clear container
    commentRef.current.innerHTML = "";

    // Create giscus script
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
