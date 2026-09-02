import { PackageSearch } from "lucide-react";
import type { Tool } from "@/types";
import { ToolCard } from "./ToolCard";

interface ToolListProps {
  tools: Tool[];
  className?: string;
  emptyTitle?: string;
  emptyDescription?: string;
}

export function ToolList({
  tools,
  className = "",
  emptyTitle = "暂无工具",
  emptyDescription = "当前筛选条件下没有匹配的工具。",
}: ToolListProps) {
  if (tools.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 px-6 text-center">
        <div className="w-16 h-16 flex items-center justify-center rounded-2xl bg-gray-100 text-gray-300 mb-4">
          <PackageSearch className="w-8 h-8" />
        </div>
        <h3 className="text-lg font-bold text-gray-700">{emptyTitle}</h3>
        <p className="text-sm text-gray-400 mt-1 max-w-sm">{emptyDescription}</p>
      </div>
    );
  }

  return (
    <div className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6 ${className}`}>
      {tools.map((tool, index) => (
        <ToolCard key={tool.id} tool={tool} index={index} />
      ))}
    </div>
  );
}
