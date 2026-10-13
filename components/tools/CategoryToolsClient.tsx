'use client';

import { useState, useMemo } from 'react';
import { ToolList } from '@/components/tools/ToolList';
import type { Tool } from '@/types';
import { calculateScoreResult } from '@/lib/scoring';
import { Filter, ArrowUpDown, Check } from 'lucide-react';

type SortOption = 'rating' | 'name' | 'updated';
type PriceFilter = 'all' | 'free' | 'freemium' | 'paid';

interface CategoryToolsClientProps {
  tools: Tool[];
}

export function CategoryToolsClient({ tools }: CategoryToolsClientProps) {
  const [sortBy, setSortBy] = useState<SortOption>('rating');
  const [priceFilter, setPriceFilter] = useState<PriceFilter>('all');
  // 分页折叠：首屏渲染前 N 张卡片，其余点 Load More 分批渲染（数据仍在客户端，筛选/排序作用于全量）
  const PAGE_SIZE = 24;
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);

  // 判断Tools的定价模式
  const getPriceMode = (tool: Tool): 'free' | 'freemium' | 'paid' => {
    const pricing = (tool as any).pricing;
    if (!pricing || pricing.length === 0) return 'freemium';

    const hasFree = pricing.some(
      (p: any) =>
        p.price?.toLowerCase().includes('free') ||
        p.name?.toLowerCase().includes('free') ||
        p.price === '$0' ||
        p.price === '0',
    );
    const hasPaid = pricing.some(
      (p: any) =>
        !p.price?.toLowerCase().includes('free') &&
        p.price !== '$0' &&
        p.price !== '0' &&
        p.price !== 'Free' &&
        p.price !== '',
    );

    if (hasFree && hasPaid) return 'freemium';
    if (hasFree) return 'free';
    return 'paid';
  };

  // 筛选和排序Tools
  const filteredAndSortedTools = useMemo(() => {
    let result = [...tools];

    // 按定价模式筛选
    if (priceFilter !== 'all') {
      result = result.filter((tool) => getPriceMode(tool) === priceFilter);
    }

    // 排序
    switch (sortBy) {
      case 'rating':
        result.sort(
          (a, b) => calculateScoreResult(b.scores).total - calculateScoreResult(a.scores).total,
        );
        break;
      case 'name':
        result.sort((a, b) => a.name.localeCompare(b.name));
        break;
      case 'updated':
        result.sort(
          (a, b) =>
            new Date((b as any).lastUpdated || '2026-01-01').getTime() -
            new Date((a as any).lastUpdated || '2026-01-01').getTime(),
        );
        break;
    }

    return result;
  }, [tools, sortBy, priceFilter]);

  // 分页切片：排序/筛选变化时重置可见数量
  const visibleTools = filteredAndSortedTools.slice(0, visibleCount);
  const resetPagination = (fn: () => void) => {
    setVisibleCount(PAGE_SIZE);
    fn();
  };

  const priceFilters: { value: PriceFilter; label: string }[] = [
    { value: 'all', label: 'All' },
    { value: 'free', label: 'Free' },
    { value: 'freemium', label: 'Freemium' },
    { value: 'paid', label: 'Paid' },
  ];

  const sortOptions: { value: SortOption; label: string }[] = [
    { value: 'rating', label: 'Top Rated' },
    { value: 'name', label: 'Name A-Z' },
    { value: 'updated', label: 'Recently Updated' },
  ];

  return (
    <div className="mb-8">
      {/* 筛选和排序Tools栏 */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 p-4 bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800">
        {/* 定价模式筛选 */}
        <div className="flex items-center gap-2 flex-wrap">
          <Filter className="w-4 h-4 text-gray-500 dark:text-gray-400 flex-shrink-0" />
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300 mr-2">Price:</span>
          <div className="flex gap-1 flex-wrap">
            {priceFilters.map((filter) => (
              <button
                key={filter.value}
                onClick={() => resetPagination(() => setPriceFilter(filter.value))}
                className={`px-3 py-1.5 text-sm rounded-lg font-medium transition-all ${
                  priceFilter === filter.value
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
                }`}
              >
                {filter.label}
              </button>
            ))}
          </div>
        </div>

        {/* 排序选项 */}
        <div className="flex items-center gap-2">
          <ArrowUpDown className="w-4 h-4 text-gray-500 dark:text-gray-400 flex-shrink-0" />
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Sort:</span>
          <select
            value={sortBy}
            onChange={(e) => resetPagination(() => setSortBy(e.target.value as SortOption))}
            className="px-3 py-1.5 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {sortOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* 结果Statistics */}
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Showing{' '}
          <span className="font-semibold text-gray-900 dark:text-white">
            {filteredAndSortedTools.length}
          </span>{' '}
          of <span className="font-semibold">{tools.length}</span> tools
          {priceFilter !== 'all' && (
            <span className="ml-1">
              · filtered by{' '}
              <span className="font-medium text-blue-600 dark:text-blue-400 capitalize">
                {priceFilter}
              </span>
            </span>
          )}
        </p>
        {priceFilter !== 'all' && (
          <button
            onClick={() => setPriceFilter('all')}
            className="text-sm text-blue-600 dark:text-blue-400 hover:underline font-medium flex items-center gap-1"
          >
            <Check className="w-3 h-3" />
            Clear filter
          </button>
        )}
      </div>

      {/* Tools列Table（分页折叠渲染） */}
      <ToolList
        tools={visibleTools}
        emptyTitle="No tools found"
        emptyDescription="Try adjusting your filters or sorting options."
      />
      {filteredAndSortedTools.length > visibleCount && (
        <div className="mt-6 flex justify-center">
          <button
            onClick={() => setVisibleCount((v) => v + PAGE_SIZE)}
            className="inline-flex items-center justify-center px-6 min-h-[44px] text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 hover:bg-blue-100 dark:hover:bg-blue-900/30 border border-blue-200 dark:border-blue-800 rounded-xl transition-colors"
          >
            Load More ({filteredAndSortedTools.length - visibleCount} more tools)
          </button>
        </div>
      )}
    </div>
  );
}
