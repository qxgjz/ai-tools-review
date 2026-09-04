"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";

interface DimensionScore {
  name: string;
  score: number;
  description: string;
}

interface ReviewTabsProps {
  dimensions: DimensionScore[];
  overallScore: number;
  grade: string;
}

export function ReviewTabs({ dimensions, overallScore, grade }: ReviewTabsProps) {
  return (
    <div className="my-8">
      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="grid w-full grid-cols-2 lg:grid-cols-4">
          <TabsTrigger value="overview">评分总览</TabsTrigger>
          <TabsTrigger value="features">功能评测</TabsTrigger>
          <TabsTrigger value="performance">性能体验</TabsTrigger>
          <TabsTrigger value="pricing">价格对比</TabsTrigger>
        </TabsList>

        {/* 评分总览 */}
        <TabsContent value="overview" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* 总分卡片 */}
            <div className="text-center p-6 bg-gray-50 dark:bg-gray-800 rounded-xl">
              <div className="text-5xl font-extrabold text-gray-900 dark:text-white mb-2">
                {overallScore.toFixed(1)}
              </div>
              <div className="text-sm text-gray-500 dark:text-gray-400 mb-3">/ 10 总分</div>
              <Badge className="text-lg px-4 py-1">{grade} 级</Badge>
            </div>

            {/* 各维度评分 */}
            <div className="md:col-span-2 space-y-4">
              {dimensions.map((dim, index) => (
                <div key={index}>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      {dim.name}
                    </span>
                    <span className="text-sm font-bold text-gray-900 dark:text-white">
                      {dim.score.toFixed(1)}/10
                    </span>
                  </div>
                  <Progress value={dim.score * 10} className="h-2" />
                </div>
              ))}
            </div>
          </div>
        </TabsContent>

        {/* 功能评测 */}
        <TabsContent value="features" className="mt-6">
          <div className="space-y-4">
            {dimensions.filter(d => d.name.includes("功能") || d.name.includes("集成")).map((dim, index) => (
              <div key={index} className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="font-semibold text-gray-900 dark:text-white">{dim.name}</h4>
                  <Badge variant="secondary">{dim.score.toFixed(1)}/10</Badge>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">{dim.description}</p>
              </div>
            ))}
          </div>
        </TabsContent>

        {/* 性能体验 */}
        <TabsContent value="performance" className="mt-6">
          <div className="space-y-4">
            {dimensions.filter(d => d.name.includes("性能") || d.name.includes("易用") || d.name.includes("体验")).map((dim, index) => (
              <div key={index} className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="font-semibold text-gray-900 dark:text-white">{dim.name}</h4>
                  <Badge variant="secondary">{dim.score.toFixed(1)}/10</Badge>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">{dim.description}</p>
              </div>
            ))}
          </div>
        </TabsContent>

        {/* 价格对比 */}
        <TabsContent value="pricing" className="mt-6">
          <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              详细的价格对比信息请参考文章中的价格对比表格。我们会定期更新各工具的最新定价和优惠信息。
            </p>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
