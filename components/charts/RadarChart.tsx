"use client";

import { useId } from "react";
import type { Score, ScoreDimension } from "@/types";

const DIMENSIONS: { key: ScoreDimension; label: string }[] = [
  { key: "functionality", label: "Functionality" },
  { key: "ux", label: "UX" },
  { key: "pricing", label: "Pricing" },
  { key: "integration", label: "Integration" },
  { key: "support", label: "Support" },
  { key: "ethics", label: "Ethics" },
];

interface RadarChartProps {
  scores: Score;
  size?: number;
  className?: string;
  showValues?: boolean;
  color?: string;
}

export function RadarChart({
  scores,
  size = 300,
  className = "",
  showValues = false,
  color = "#3b82f6",
}: RadarChartProps) {
  const gradientId = useId();
  const cx = size / 2;
  const cy = size / 2;
  const padding = 55;
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

  const dataPoints = DIMENSIONS.map((dim, i) => {
    const score = clampScore(scores[dim.key] ?? 0);
    const r = radius * (score / 10);
    const p = polarToCartesian(getAngle(i), r);
    return { x: p.x, y: p.y, score, dim: dim.key };
  });
  const dataPointsStr = dataPoints.map((p) => `${p.x.toFixed(2)},${p.y.toFixed(2)}`).join(" ");

  const gridLevels = [2, 4, 6, 8, 10];

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className={className} role="img" aria-label="Six-dimension capability radar chart">
      <defs>
        <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor={color} stopOpacity="0.25" />
          <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.25" />
        </linearGradient>
      </defs>

      {gridLevels.map((level) => (
        <polygon key={level} points={getHexPoints(radius * (level / 10))} fill="none" stroke="#e5e7eb" strokeWidth="1" />
      ))}

      {gridLevels.map((level) => {
        const p = polarToCartesian(getAngle(0), radius * (level / 10));
        return (
          <text key={`l-${level}`} x={p.x.toFixed(2)} y={(p.y - 4).toFixed(2)} textAnchor="middle" fontSize="9" fill="#9ca3af">
            {level}
          </text>
        );
      })}

      {DIMENSIONS.map((_, i) => {
        const p = polarToCartesian(getAngle(i), radius);
        return <line key={`a-${i}`} x1={cx} y1={cy} x2={p.x.toFixed(2)} y2={p.y.toFixed(2)} stroke="#d1d5db" strokeWidth="1" />;
      })}

      <polygon
        points={dataPointsStr}
        fill={`url(#${gradientId})`}
        stroke={color}
        strokeWidth="2.5"
        strokeLinejoin="round"
        style={{ strokeDasharray: 1200, strokeDashoffset: 1200, animation: "radar-draw 1.2s ease-out 0.15s forwards" }}
      />

      {dataPoints.map((p, i) => (
        <circle
          key={`d-${p.dim}`}
          cx={p.x.toFixed(2)}
          cy={p.y.toFixed(2)}
          r="4.5"
          fill={color}
          stroke="white"
          strokeWidth="2.5"
          style={{ opacity: 0, animation: `radar-fade-in 0.4s ease-out ${0.9 + i * 0.08}s forwards` }}
        />
      ))}

      {showValues &&
        dataPoints.map((p, i) => {
          // 修复：将Rating值放在数据点内侧（-14），避免与外侧维度Tags重叠
          const valueRadius = Math.max(0, p.score / 10 * radius - 14);
          const lp = polarToCartesian(getAngle(i), valueRadius);
          return (
            <text
              key={`v-${p.dim}`}
              x={lp.x.toFixed(2)}
              y={lp.y.toFixed(2)}
              textAnchor="middle"
              dominantBaseline="middle"
              fontSize="10"
              fontWeight="700"
              fill={color}
              style={{ opacity: 0, animation: `radar-fade-in 0.3s ease-out ${1.2 + i * 0.05}s forwards` }}
            >
              {p.score.toFixed(1)}
            </text>
          );
        })}

      {DIMENSIONS.map((dim, i) => {
        const angle = getAngle(i);
        const p = polarToCartesian(angle, radius + 26);
        const cosVal = Math.cos(angle);
        const anchor = cosVal > 0.3 ? "start" : cosVal < -0.3 ? "end" : "middle";
        return (
          <text key={`c-${dim.key}`} x={p.x.toFixed(2)} y={p.y.toFixed(2)} textAnchor={anchor} dominantBaseline="middle" fontSize="11.5" fill="#4b5563" fontWeight="600">
            {dim.label}
          </text>
        );
      })}

      <style>{`
        @keyframes radar-draw { to { stroke-dashoffset: 0; } }
        @keyframes radar-fade-in { to { opacity: 1; } }
      `}</style>
    </svg>
  );
}
