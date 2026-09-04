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

export default function ReviewTabs({ dimensions, overallScore, grade }: ReviewTabsProps) {
  return (
    <div className="my-8">
      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="grid w-full grid-cols-2 lg:grid-cols-4">
          <TabsTrigger value="overview">Score Overview</TabsTrigger>
          <TabsTrigger value="features">Feature Review</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="pricing">Pricing</TabsTrigger>
        </TabsList>

        {/* Score Overview */}
        <TabsContent value="overview" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Total Score Card */}
            <div className="text-center p-6 bg-gray-50 dark:bg-gray-800 rounded-xl">
              <div className="text-5xl font-extrabold text-gray-900 dark:text-white mb-2">
                {overallScore.toFixed(1)}
              </div>
              <div className="text-sm text-gray-500 dark:text-gray-400 mb-3">/ 10 Total</div>
              <Badge className="text-lg px-4 py-1">{grade} Grade</Badge>
            </div>

            {/* Dimension Scores */}
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

        {/* Feature Review */}
        <TabsContent value="features" className="mt-6">
          <div className="space-y-4">
            {dimensions.filter(d => d.name.toLowerCase().includes("function") || d.name.toLowerCase().includes("integration") || d.name.toLowerCase().includes("feature")).map((dim, index) => (
              <div key={index} className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="font-semibold text-gray-900 dark:text-white">{dim.name}</h4>
                  <Badge variant="secondary">{dim.score.toFixed(1)}/10</Badge>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">{dim.description}</p>
              </div>
            ))}
            {dimensions.filter(d => d.name.toLowerCase().includes("function") || d.name.toLowerCase().includes("integration") || d.name.toLowerCase().includes("feature")).length === 0 && (
              <p className="text-sm text-gray-500 dark:text-gray-400">Feature dimension details will be displayed here.</p>
            )}
          </div>
        </TabsContent>

        {/* Performance */}
        <TabsContent value="performance" className="mt-6">
          <div className="space-y-4">
            {dimensions.filter(d => d.name.toLowerCase().includes("performance") || d.name.toLowerCase().includes("ux") || d.name.toLowerCase().includes("experience") || d.name.toLowerCase().includes("speed")).map((dim, index) => (
              <div key={index} className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="font-semibold text-gray-900 dark:text-white">{dim.name}</h4>
                  <Badge variant="secondary">{dim.score.toFixed(1)}/10</Badge>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">{dim.description}</p>
              </div>
            ))}
            {dimensions.filter(d => d.name.toLowerCase().includes("performance") || d.name.toLowerCase().includes("ux") || d.name.toLowerCase().includes("experience") || d.name.toLowerCase().includes("speed")).length === 0 && (
              <p className="text-sm text-gray-500 dark:text-gray-400">Performance dimension details will be displayed here.</p>
            )}
          </div>
        </TabsContent>

        {/* Pricing */}
        <TabsContent value="pricing" className="mt-6">
          <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              For detailed pricing comparison, please refer to the pricing comparison table in the article. We regularly update the latest pricing and promotional information for each tool.
            </p>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
