"use client";

import { useEffect, useState, useRef } from "react";
import { List, ChevronRight } from "lucide-react";

interface TocItem {
  id: string;
  text: string;
  level: number;
}

interface TableOfContentsProps {
  contentHtml: string;
  className?: string;
}

/**
 * TableOfContents - 文章目录组件
 * 基于GitHub高星博客项目最佳实践：
 * - 自动从HTML内容提取h2/h3标题
 * - 滚动时高亮当前章节
 * - 点击平滑滚动到对应位置
 * - 桌面端右侧固定，移动端可折叠
 */
export function TableOfContents({ contentHtml, className = "" }: TableOfContentsProps) {
  const [headings, setHeadings] = useState<TocItem[]>([]);
  const [activeId, setActiveId] = useState<string>("");
  const [isOpen, setIsOpen] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);

  // 从HTML中提取标题并生成ID
  useEffect(() => {
    if (!contentHtml) return;

    const parser = new DOMParser();
    const doc = parser.parseFromString(contentHtml, "text/html");
    const headingElements = doc.querySelectorAll("h2, h3");

    const items: TocItem[] = [];
    headingElements.forEach((heading, index) => {
      const text = heading.textContent?.trim() || "";
      if (!text) return;

      // 生成URL友好的ID
      const id = text
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, "")
        .replace(/\s+/g, "-")
        .substring(0, 50);

      items.push({
        id: id || `heading-${index}`,
        text,
        level: heading.tagName === "H2" ? 2 : 3,
      });
    });

    setHeadings(items);
  }, [contentHtml]);

  // 滚动监听 - 高亮当前章节
  useEffect(() => {
    if (headings.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        });
      },
      {
        rootMargin: "-20% 0px -70% 0px",
        threshold: 0,
      }
    );

    // 给页面中的标题元素添加ID
    headings.forEach((item) => {
      const elements = document.querySelectorAll(`h2, h3`);
      elements.forEach((el) => {
        const text = el.textContent?.trim() || "";
        const generatedId = text
          .toLowerCase()
          .replace(/[^a-z0-9\s-]/g, "")
          .replace(/\s+/g, "-")
          .substring(0, 50);
        if (generatedId === item.id && !el.id) {
          el.id = item.id;
          (el as HTMLElement).style.scrollMarginTop = "80px";
        }
      });
    });

    // 观察所有标题元素
    headings.forEach((item) => {
      const el = document.getElementById(item.id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [headings]);

  const handleClick = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" });
      setIsOpen(false);
    }
  };

  if (headings.length === 0) return null;

  return (
    <div className={`${className}`}>
      {/* 移动端折叠按钮 */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden w-full flex items-center justify-between px-4 py-3 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 mb-4"
      >
        <span className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
          <List className="w-4 h-4" />
          Table of Contents
        </span>
        <ChevronRight
          className={`w-4 h-4 text-gray-500 transition-transform ${isOpen ? "rotate-90" : ""}`}
        />
      </button>

      {/* 目录内容 */}
      <nav
        className={`${
          isOpen ? "block" : "hidden"
        } lg:block bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-200 dark:border-gray-800 p-4`}
      >
        <h3 className="hidden lg:flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-3">
          <List className="w-3.5 h-3.5" />
          On this page
        </h3>
        <ul className="space-y-1">
          {headings.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => handleClick(item.id)}
                className={`w-full text-left text-sm py-1.5 px-2 rounded-md transition-all duration-200 ${
                  item.level === 3 ? "pl-6" : ""
                } ${
                  activeId === item.id
                    ? "text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 font-medium"
                    : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800"
                }`}
              >
                {item.text}
              </button>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}
