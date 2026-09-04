import Link from "next/link";
import { ChevronRight, Home } from "lucide-react";

interface BreadcrumbItem {
  name: string;
  url?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  className?: string;
}

/**
 * Breadcrumb - 可视化面包屑导航Component
 * 帮助用户了解当前Page位置，提升User Experience和SEO
 */
export function Breadcrumb({ items, className = "" }: BreadcrumbProps) {
  return (
    <nav
      aria-label="Breadcrumb"
      className={`flex items-center flex-wrap gap-1 text-sm text-gray-500 dark:text-gray-400 ${className}`}
    >
      {/* Home链接 */}
      <Link
        href="/"
        className="flex items-center gap-1 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
      >
        <Home className="w-3.5 h-3.5" />
        <span className="hidden sm:inline">Home</span>
      </Link>

      {/* 面包屑项 */}
      {items.map((item, index) => (
        <div key={index} className="flex items-center gap-1">
          <ChevronRight className="w-3.5 h-3.5 text-gray-300 dark:text-gray-600 flex-shrink-0" />
          {item.url && index < items.length - 1 ? (
            <Link
              href={item.url}
              className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors truncate max-w-[150px]"
            >
              {item.name}
            </Link>
          ) : (
            <span className="text-gray-900 dark:text-white font-medium truncate max-w-[200px]">
              {item.name}
            </span>
          )}
        </div>
      ))}
    </nav>
  );
}
