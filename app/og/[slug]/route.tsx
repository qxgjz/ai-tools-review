import { ImageResponse } from "@vercel/og";
import toolsData from "@/data/tools.json";
import { calculateScoreResult } from "@/lib/scoring";
import type { Grade } from "@/types";

export const runtime = "edge";

const GRADE_COLORS: Record<Grade, { bg: string; text: string; label: string }> = {
  S: { bg: "#f59e0b", text: "#ffffff", label: "Excellent" },
  A: { bg: "#10b981", text: "#ffffff", label: "Great" },
  B: { bg: "#3b82f6", text: "#ffffff", label: "Good" },
  C: { bg: "#eab308", text: "#ffffff", label: "Average" },
  D: { bg: "#ef4444", text: "#ffffff", label: "Poor" },
  F: { bg: "#6b7280", text: "#ffffff", label: "Not Recommended" },
};

const DIMENSION_LABELS_OG = ["Functionality", "User Experience", "Pricing & Value", "Integrations", "Support & Reliability", "Ethics & Transparency"];

export async function GET(_request: Request, { params }: { params: { slug: string } }) {
  const tool = toolsData.find((t) => t.slug === params.slug);

  if (!tool) {
    return new ImageResponse(
      (
        <div style={{ width: "100%", height: "100%", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", background: "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #6366f1 100%)", fontFamily: "sans-serif" }}>
          <div style={{ width: 120, height: 120, borderRadius: 28, background: "white", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 56, fontWeight: 900, color: "#1e40af", marginBottom: 32 }}>AI</div>
          <div style={{ fontSize: 72, fontWeight: 800, color: "white", marginBottom: 16 }}>AIToolCrux</div>
          <div style={{ fontSize: 28, color: "rgba(255,255,255,0.85)" }}>Six-Dimension Scoring · Expert Reviews · Smart Recommendations</div>
        </div>
      ),
      { width: 1200, height: 630 }
    );
  }

  const { total, grade } = calculateScoreResult(tool.scores);
  const gradeColor = GRADE_COLORS[grade];

  return new ImageResponse(
    (
      <div style={{ width: "100%", height: "100%", display: "flex", flexDirection: "column", background: "linear-gradient(135deg, #1e3a8a 0%, #2563eb 35%, #4f46e5 70%, #7c3aed 100%)", fontFamily: "sans-serif", padding: "56px 64px", position: "relative" }}>
        <div style={{ position: "absolute", top: -80, right: -60, width: 320, height: 320, borderRadius: 999, background: "rgba(255,255,255,0.07)" }} />
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 36, position: "relative", zIndex: 1 }}>
          <div style={{ display: "flex", alignItems: "center" }}>
            <div style={{ width: 52, height: 52, borderRadius: 14, background: "white", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 26, fontWeight: 900, color: "#1e40af", marginRight: 14 }}>AI</div>
            <div style={{ fontSize: 26, fontWeight: 700, color: "white" }}>AIToolCrux</div>
          </div>
          <div style={{ padding: "8px 20px", background: "rgba(255,255,255,0.15)", borderRadius: 999, fontSize: 18, color: "white", fontWeight: 500 }}>{tool.category}</div>
        </div>

        <div style={{ flex: 1, background: "white", borderRadius: 28, padding: "44px 48px", display: "flex", flexDirection: "column", justifyContent: "center", boxShadow: "0 30px 60px -15px rgba(0,0,0,0.3)", position: "relative", zIndex: 1 }}>
          <div style={{ fontSize: 22, color: "#6b7280", fontWeight: 500, marginBottom: 10 }}>{tool.vendor}</div>
          <div style={{ display: "flex", alignItems: "center", marginBottom: 20, flexWrap: "wrap" }}>
            <div style={{ fontSize: 60, fontWeight: 900, color: "#111827", marginRight: 24, letterSpacing: -1 }}>{tool.name}</div>
            <div style={{ padding: "14px 28px", borderRadius: 14, background: gradeColor.bg, color: gradeColor.text, fontSize: 30, fontWeight: 800 }}>Grade {grade} · {gradeColor.label}</div>
          </div>
          <div style={{ fontSize: 23, color: "#4b5563", lineHeight: 1.5, marginBottom: 28, maxWidth: 820 }}>{tool.description.length > 80 ? tool.description.slice(0, 80) + "..." : tool.description}</div>
          <div style={{ display: "flex", alignItems: "flex-end" }}>
            <div style={{ fontSize: 100, fontWeight: 900, color: "#1e40af", lineHeight: 1, letterSpacing: -2 }}>{total.toFixed(1)}</div>
            <div style={{ fontSize: 28, color: "#9ca3af", marginLeft: 14, marginBottom: 14, fontWeight: 500 }}>/ 10<div style={{ fontSize: 18, color: "#d1d5db", marginTop: 4 }}>Overall Score</div></div>
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "center", gap: 14, marginTop: 32, position: "relative", zIndex: 1 }}>
          {DIMENSION_LABELS_OG.map((dim) => (
            <div key={dim} style={{ padding: "8px 18px", background: "rgba(255,255,255,0.12)", borderRadius: 999, fontSize: 17, color: "rgba(255,255,255,0.9)", fontWeight: 500 }}>{dim}</div>
          ))}
        </div>
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
