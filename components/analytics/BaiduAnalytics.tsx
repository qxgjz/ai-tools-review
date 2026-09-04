"use client";

import Script from "next/script";

/**
 * 百度统计组件
 *
 * 使用方法：
 * 1. 在百度统计平台（https://tongji.baidu.com）注册账号并添加网站
 * 2. 获取统计代码中的 siteId（通常是 hm.js?后面的参数，如 "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"）
 * 3. 将 siteId 填入下方 BAIDU_SITE_ID 常量
 * 4. 在 layout.tsx 中引入此组件
 *
 * 注意：当前 BAIDU_SITE_ID 为空，组件不会加载任何脚本。
 * 填入有效的 siteId 后，百度统计脚本会自动加载。
 */

// 百度统计 siteId（请填入你的百度统计 siteId）
const BAIDU_SITE_ID = process.env.NEXT_PUBLIC_BAIDU_SITE_ID || "";

export function BaiduAnalytics() {
  // 如果没有配置 siteId，不加载任何脚本
  if (!BAIDU_SITE_ID) {
    return null;
  }

  return (
    <>
      {/* 百度统计主脚本 */}
      <Script id="baidu-tongji" strategy="afterInteractive">
        {`
          var _hmt = _hmt || [];
          (function() {
            var hm = document.createElement("script");
            hm.src = "https://hm.baidu.com/hm.js?${BAIDU_SITE_ID}";
            var s = document.getElementsByTagName("script")[0];
            s.parentNode.insertBefore(hm, s);
          })();
        `}
      </Script>
    </>
  );
}

/**
 * 百度统计事件追踪函数
 * 在客户端组件中调用：
 *   import { baiduTrackEvent } from "@/components/analytics/BaiduAnalytics";
 *   baiduTrackEvent("category", "action", "label", value);
 */
export function baiduTrackEvent(
  category: string,
  action: string,
  label?: string,
  value?: number
) {
  if (typeof window === "undefined") return;
  if (!(window as any)._hmt) return;

  const params: (string | number)[] = [category, action];
  if (label !== undefined) params.push(label);
  if (value !== undefined) params.push(value);

  (window as any)._hmt.push(["_trackEvent", ...params]);
}
