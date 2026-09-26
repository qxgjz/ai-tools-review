'use client';

import { useEffect } from 'react';
import type { Metric } from 'web-vitals';

/**
 * Web Vitals Real User Monitoring (RUM)
 * Reports LCP / INP / CLS to Google Analytics 4 as events.
 * Accumulates 7 days of real-user data before optimizing.
 *
 * Core Web Vitals 2026 thresholds:
 * - LCP: <= 2.5s (good), 2.5-4s (needs improvement), > 4s (poor)
 * - INP: <= 200ms (good), 200-500ms (needs improvement), > 500ms (poor)
 * - CLS: <= 0.1 (good), 0.1-0.25 (needs improvement), > 0.25 (poor)
 */

function sendToAnalytics(metric: Metric) {
  const { name, value, rating, id } = metric;

  // Log to console for debugging
  if (process.env.NODE_ENV === 'development') {
    console.log(`[WebVitals] ${name}: ${Math.round(value)} (${rating})`);
  }

  // Send to GA4 as events
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const w = window as any;
  if (typeof w.gtag === 'function') {
    w.gtag('event', name, {
      event_category: 'Web Vitals',
      value: Math.round(name === 'CLS' ? value * 1000 : value),
      metric_id: id,
      metric_value: value,
      metric_rating: rating,
      non_interaction: true,
    });
  }

  // Also store in localStorage for local debugging
  try {
    const key = 'wv_metrics';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    existing.push({ name, value: Math.round(value), rating, id, ts: Date.now() });
    // Keep last 50 entries
    if (existing.length > 50) existing.shift();
    localStorage.setItem(key, JSON.stringify(existing));
  } catch {
    // localStorage may be unavailable
  }
}

export default function WebVitalsReporter() {
  useEffect(() => {
    // Dynamically import web-vitals to keep bundle small
    import('web-vitals').then(({ onLCP, onINP, onCLS, onFCP, onTTFB }) => {
      onLCP(sendToAnalytics);
      onINP(sendToAnalytics);
      onCLS(sendToAnalytics);
      onFCP(sendToAnalytics);
      onTTFB(sendToAnalytics);
    });
  }, []);

  return null;
}
