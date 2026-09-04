"use client";

import { useId } from "react";
import type { Score, ScoreDimension } from "@/types";

const DIMENSIONS: { key: ScoreDimension; label: string }[] = [
  { key: "functionality", label: "Functionality" },
  { key: "ux", label: "User Experience" },
  { key: "pricing", label: "Pricing & Value" },
  { key: "integration", label: "Integrations" },
  { key: "support", label: "Support & Reliability" },
  { key: "ethics", label: "Ethics & Transparency" },
];

interface ToolData {
  name: string;
  scores: Score;
  color: string;
}

interface MultiRadarChartProps {
  tools: ToolData[];
  size?: number;
  className?: string;
}

const COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"];

export function MultiRadarChart({
  tools,
  size = 400,
  className = "",
}: MultiRadarChartProps) {
  const gradientId = useId();
  const cx = size / 2;
  const cy = size / 2;
  const padding = 50;
  const radius = size / 2 - padding;
  const n = 6;

  const getAngle = (i: number) => (-90 + i * (360 / n)) * (Math.PI / 180);
  const polarToCartesian = (angle: number, r: number) => ({
    x: cx + r * Math.cos(angle),
    y: cy + r * Math.sin(angle),
  });
  const getHexPoints = (r: number) =>
    Array.from({ length: n }, (_, i) => {
      const p = polarToCartesian(getAngle(i), r);
      return `${p.x.toFixed(2)},${p.y.toFixed(2)}`;
    }).join(" ");

  const clampScore = (val: number) => Math.min(10, Math.max(0, val));
  const gridLevels = [2, 4, 6, 8, 10];

  const toolsWithColor = tools.map((t, i) => ({
    ...t,
    color: t.color || COLORS[i % COLORS.length],
  }));

  return (
    <div className="flex flex-col items-center">
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className={className}
        role="img"
        aria-label="多工具六维能力雷达图对比"
      >
        {/* 网格背景 */}
        {gridLevels.map((level) => (
          <polygon
            key={level}
            points={getHexPoints(radius * (level / 10))}
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="1"
            className="dark:stroke-gray-700"
          />
        ))}

        {/* 网格刻度文字 */}
        {gridLevels.map((level) => {
          const p = polarToCartesian(getAngle(0), radius * (level / 10));
          return (
            <text
              key={`l-${level}`}
              x={p.x.toFixed(2)}
              y={(p.y - 4).toFixed(2)}
              textAnchor="middle"
              fontSize="9"
              fill="#9ca3af"
            >
              {level}
            </text>
          );
        })}

        {/* 轴线 */}
        {DIMENSIONS.map((_, i) => {
          const p = polarToCartesian(getAngle(i), radius);
          return (
            <line
              key={`a-${i}`}
              x1={cx}
              y1={cy}
              x2={p.x.toFixed(2)}
              y2={p.y.toFixed(2)}
              stroke="#d1d5db"
              strokeWidth="1"
              className="dark:stroke-gray-600"
            />
          );
        })}

        {/* 各工具数据多边形 */}
        {toolsWithColor.map((tool, toolIdx) => {
          const dataPoints = DIMENSIONS.map((dim) => {
            const score = clampScore(tool.scores[dim.key] ?? 0);
            const r = radius * (score / 10);
            const angle = getAngle(DIMENSIONS.indexOf(dim));
            const p = polarToCartesian(angle, r);
            return { x: p.x, y: p.y, score };
          });
          const dataPointsStr = dataPoints
            .map((p) => `${p.x.toFixed(2)},${p.y.toFixed(2)}`)
            .join(" ");

          return (
            <g key={tool.name}>
              <polygon
                points={dataPointsStr}
                fill={tool.color}
                fillOpacity="0.12"
                stroke={tool.color}
                strokeWidth="2.5"
                strokeLinejoin="round"
              />
              {dataPoints.map((p, i) => (
                <circle
                  key={`d-${tool.name}-${i}`}
                  cx={p.x.toFixed(2)}
                  cy={p.y.toFixed(2)}
                  r="4"
                  fill={tool.color}
                  stroke="white"
                  strokeWidth="2"
                />
              ))}
            </g>
          );
        })}

        {/* 维度标签 */}
        {DIMENSIONS.map((dim, i) => {
          const angle = getAngle(i);
          const p = polarToCartesian(angle, radius + 28);
          const cosVal = Math.cos(angle);
          const anchor = cosVal > 0.3 ? "start" : cosVal < -0.3 ? "end" : "middle";
          return (
            <text
              key={`c-${dim.key}`}
              x={p.x.toFixed(2)}
              y={p.y.toFixed(2)}
              textAnchor={anchor}
              dominantBaseline="middle"
              fontSize="12"
              fill="#4b5563"
              fontWeight="600"
              className="dark:text-gray-300"
            >
              {dim.label}
            </text>
          );
        })}
      </svg>

      {/* 图例 */}
      <div className="flex flex-wrap justify-center gap-4 mt-4">
        {toolsWithColor.map((tool) => (
          <div key={tool.name} className="flex items-center gap-2">
            <span
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: tool.color }}
            />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {tool.name}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
