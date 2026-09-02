import type { Metadata } from "next";
import Script from "next/script";
import "./globals.css";
import { Header } from "@/components/layout/Header";

export const metadata: Metadata = {
  title: "AI工具测评台 - 专业AI工具六维测评与导航",
  description: "基于六维加权评分模型，为你精选最优质的AI工具。覆盖对话、写作、绘画、编程、视频、办公等全品类。",
  keywords: ["AI工具", "AI测评", "AI导航", "ChatGPT", "Midjourney", "AI工具推荐"],
  verification: {
    google: "npnKpSTQ27It6K-ajF27C1ZArzyIbSUhFlgQFS02-gs",
    other: {
      "baidu-site-verification": "codeva-UVziTZwCm7",
    },
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen bg-gray-50">
        {/* Umami 网站分析 */}
        <Script
          defer
          src="https://cloud.umami.is/script.js"
          data-website-id="7d417a27-1151-407a-9bbb-ef8dd10189a2"
        />
        <Header />
        <main className="pt-16">{children}</main>
        <footer className="mt-16 py-8 border-t border-gray-100 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 text-center">
            <p className="text-sm text-gray-400">
              AI工具测评台 · 评分基于公开测评方法论，联盟链接收入不影响评分
            </p>
            <p className="text-xs text-gray-300 mt-2">
              © 2026 AI Tools Review. All rights reserved.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
