'use client';

import Link from 'next/link';
import { ArrowUpRight, Sparkles } from 'lucide-react';
import type { Tool, Grade } from '@/types';
import { calculateScoreResult } from '@/lib/scoring';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

/* 等级徽章：纯色状态色（无渐变），design_standard 状态色体系 */
const GRADE_STYLES: Record<Grade, string> = {
  S: 'bg-[#b45309] text-white',
  A: 'bg-[#15803d] text-white',
  B: 'bg-[#5E6AD2] text-white',
  C: 'bg-[#a16207] text-white',
  D: 'bg-[#b91c1c] text-white',
  F: 'bg-[#52525b] text-white',
};

const GRADE_BAR_COLORS: Record<Grade, string> = {
  S: 'bg-[#b45309]',
  A: 'bg-[#15803d]',
  B: 'bg-[#5E6AD2]',
  C: 'bg-[#a16207]',
  D: 'bg-[#b91c1c]',
  F: 'bg-[#52525b]',
};

interface ToolCardProps {
  tool: Tool;
  index?: number;
}

export function ToolCardV2({ tool, index = 0 }: ToolCardProps) {
  const { total, grade } = calculateScoreResult(tool.scores);
  const scorePercent = Math.min((total / 10) * 100, 100);
  const isFeatured = total >= 8.5;

  return (
    <div className="h-full group">
      <Link href={`/tools/${tool.slug}`} className="block h-full">
        <Card className="relative h-full flex flex-col overflow-hidden rounded-lg border hover:border-[rgba(0,0,0,0.12)] hover:shadow-md dark:hover:border-white/20 transition-all duration-150 ease-[cubic-bezier(0.16,1,0.3,1)] hover:-translate-y-1">
          {/* FeaturedTags */}
          {isFeatured && (
            <div className="absolute top-3 right-3 z-10">
              <Badge className="bg-[#F59E0B] text-white border-0">
                <Sparkles className="w-3 h-3 mr-1" />
                TOP
              </Badge>
            </div>
          )}

          <CardHeader className="pb-4">
            {/* 头部：Logo + 等级 */}
            <div className="flex items-start justify-between">
              <div className="w-12 h-12 flex items-center justify-center rounded-lg bg-secondary text-foreground text-lg font-semibold overflow-hidden">
                {tool.screenshot ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={tool.screenshot}
                    alt={`${tool.name} screenshot`}
                    width={48}
                    height={48}
                    loading="lazy"
                    className="w-12 h-12 object-cover"
                  />
                ) : (
                  tool.name.charAt(0).toUpperCase()
                )}
              </div>
              <span
                className={`px-2.5 py-1 rounded-md text-sm font-semibold ${GRADE_STYLES[grade]}`}
              >
                {grade}
              </span>
            </div>

            {/* 名称 + 厂商 */}
            <div className="mt-4">
              <CardTitle className="text-base font-semibold tracking-tight group-hover:text-primary transition-colors line-clamp-1">
                {tool.name}
              </CardTitle>
              <CardDescription className="mt-0.5 text-xs">{tool.vendor}</CardDescription>
            </div>

            {/* CategoriesTags */}
            <div className="mt-2">
              <Badge variant="outline" className="text-xs font-normal">
                {tool.category}
              </Badge>
            </div>
          </CardHeader>

          <CardContent className="flex-1">
            {/* 描述 */}
            <p className="text-sm text-foreground/60 leading-relaxed line-clamp-2">
              {tool.description}
            </p>
          </CardContent>

          <CardFooter className="pt-4 border-t">
            <div className="w-full">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-baseline gap-1">
                  <span className="text-2xl font-semibold tracking-tight text-foreground tabular-nums">
                    {total.toFixed(1)}
                  </span>
                  <span className="text-xs text-foreground/45">/10</span>
                </div>
                <div className="w-8 h-8 flex items-center justify-center rounded-full bg-secondary text-foreground/45 group-hover:bg-primary group-hover:text-white group-hover:scale-110 transition-all duration-150">
                  <ArrowUpRight className="w-4 h-4" />
                </div>
              </div>
              {/* Rating进度条 - shadcn/ui Progress */}
              <Progress
                value={scorePercent}
                className="h-1.5"
                indicatorClassName={GRADE_BAR_COLORS[grade]}
              />
            </div>
          </CardFooter>
        </Card>
      </Link>
    </div>
  );
}
