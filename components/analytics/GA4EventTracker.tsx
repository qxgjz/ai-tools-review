"use client";

import { useEffect } from "react";

declare global {
  interface Window {
    dataLayer: any[];
    gtag: (...args: any[]) => void;
  }
}

export function GA4EventTracker() {
  useEffect(() => {
    // 确保 gtag 可用
    if (typeof window === "undefined" || !window.gtag) return;

    // 1. 外链点击追踪
    const handleClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      const link = target.closest("a");
      if (!link) return;

      const href = link.getAttribute("href");
      if (!href) return;

      // 检测外链
      const isExternal = href.startsWith("http") && !href.includes("aitoolcrux.com");
      if (isExternal) {
        window.gtag("event", "outbound_click", {
          outbound_url: href,
          link_text: link.textContent?.trim().substring(0, 100) || "unknown",
        });
      }

      // 检测联盟链接点击
      const affiliateLinks = ["affiliate", "ref", "partner", "utm_source"];
      if (isExternal && affiliateLinks.some((p) => href.toLowerCase().includes(p))) {
        window.gtag("event", "affiliate_click", {
          outbound_url: href,
          link_text: link.textContent?.trim().substring(0, 100) || "unknown",
        });
      }
    };

    // 2. 滚动深度追踪
    const scrollDepths = [25, 50, 75, 100];
    const trackedDepths = new Set<number>();

    const handleScroll = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (docHeight <= 0) return;

      const scrollPercent = Math.round((scrollTop / docHeight) * 100);

      for (const depth of scrollDepths) {
        if (scrollPercent >= depth && !trackedDepths.has(depth)) {
          trackedDepths.add(depth);
          window.gtag("event", "scroll_depth", {
            scroll_percent: depth,
            page_path: window.location.pathname,
          });
        }
      }
    };

    // 3. 工具选择追踪（compare页面）
    const handleToolSelect = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      const toolButton = target.closest("button");
      if (!toolButton) return;

      // 检测是否是工具选择按钮（在 compare 页面）
      if (window.location.pathname === "/compare") {
        const toolName = toolButton.querySelector("span")?.textContent?.trim();
        if (toolName && toolName.length < 50) {
          window.gtag("event", "tool_selected", {
            tool_name: toolName,
            page_path: "/compare",
          });
        }
      }
    };

    document.addEventListener("click", handleClick);
    document.addEventListener("click", handleToolSelect);
    window.addEventListener("scroll", handleScroll, { passive: true });

    return () => {
      document.removeEventListener("click", handleClick);
      document.removeEventListener("click", handleToolSelect);
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return null;
}
