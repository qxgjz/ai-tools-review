"use client";

import { useEffect, useRef } from "react";

declare global {
  interface Window {
    adsbygoogle: any[];
  }
}

interface AdSlotProps {
  slot?: string;
  format?: "auto" | "horizontal" | "vertical" | "rectangle";
  className?: string;
  label?: string;
}

/**
 * AdSense广告位组件
 * 预留广告位，接入AdSense后自动显示广告
 * 当前为占位符，配置AdSense publisher ID后自动启用
 */
export function AdSlot({ slot = "0000000000", format = "auto", className = "", label }: AdSlotProps) {
  const adRef = useRef<HTMLModElement>(null);
  const loaded = useRef(false);

  useEffect(() => {
    // 只有在配置了真实的AdSense slot后才加载广告
    if (slot !== "0000000000" && adRef.current && !loaded.current) {
      try {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
        loaded.current = true;
      } catch (e) {
        console.error("AdSense error:", e);
      }
    }
  }, [slot]);

  // 如果未配置真实slot，显示占位符
  if (slot === "0000000000") {
    return (
      <div className={`my-6 ${className}`}>
        <div className="border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-lg p-8 text-center bg-gray-50 dark:bg-gray-900/50">
          <p className="text-xs text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1">
            {label || "Advertisement"}
          </p>
          <p className="text-sm text-gray-400 dark:text-gray-500">
            Ad Space — Configure Google AdSense to display ads here
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`my-6 ${className}`}>
      {label && (
        <p className="text-xs text-gray-400 dark:text-gray-500 uppercase tracking-wider text-center mb-2">
          {label}
        </p>
      )}
      <ins
        ref={adRef}
        className="adsbygoogle"
        style={{ display: "block" }}
        data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
        data-ad-slot={slot}
        data-ad-format={format}
        data-full-width-responsive="true"
      />
    </div>
  );
}

/**
 * 文章内联广告（文章中部）
 */
export function InArticleAd({ slot = "0000000000" }: { slot?: string }) {
  return <AdSlot slot={slot} format="auto" label="Sponsored" className="max-w-2xl mx-auto" />;
}

/**
 * 页头横幅广告
 */
export function HeaderBannerAd({ slot = "0000000000" }: { slot?: string }) {
  return <AdSlot slot={slot} format="horizontal" label="Advertisement" className="max-w-4xl mx-auto" />;
}
