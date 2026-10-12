'use client';

import { useEffect, useState } from 'react';
import { List, ChevronRight } from 'lucide-react';

export interface TocItem {
  id: string;
  text: string;
  level: number;
}

interface TableOfContentsProps {
  headings: TocItem[];
  className?: string;
}

/**
 * TableOfContents - 文章目录组件
 * - 标题列表由服务端从 Markdown 提取传入（避免全量正文进 RSC payload）
 * - 滚动时高亮当前章节
 * - 点击平滑滚动到对应位置
 * - 桌面端右侧固定，移动端可折叠
 */
export function TableOfContents({ headings, className = '' }: TableOfContentsProps) {
  const [activeId, setActiveId] = useState<string>('');
  const [isOpen, setIsOpen] = useState(false);

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
        rootMargin: '-20% 0px -70% 0px',
        threshold: 0,
      },
    );

    // 正文标题 id 由服务端 markdownToHtml 生成（与 headings 中 id 同规则）
    headings.forEach((item) => {
      const el = document.getElementById(item.id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [headings]);

  const handleClick = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
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
          className={`w-4 h-4 text-gray-500 transition-transform ${isOpen ? 'rotate-90' : ''}`}
        />
      </button>

      {/* 目录内容 */}
      <nav
        className={`${
          isOpen ? 'block' : 'hidden'
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
                  item.level === 3 ? 'pl-6' : ''
                } ${
                  activeId === item.id
                    ? 'text-emerald-600 dark:text-emerald-400 bg-blue-50 dark:bg-emerald-900/20 font-medium'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'
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
