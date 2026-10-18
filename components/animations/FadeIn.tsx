import type { ReactNode } from 'react';

interface FadeInProps {
  children: ReactNode;
  delay?: number;
  duration?: number;
  x?: number;
  y?: number;
  className?: string;
  once?: boolean;
}

/**
 * FadeIn - pure CSS entrance animation (no framer-motion dependency).
 * Uses `fade-in-up` keyframes with `both` fill mode so elements always end
 * visible. Initial opacity:0 only applies during the animation delay, and
 * below-fold elements have finished animating by the time the user scrolls
 * to them. Never wrap above-the-fold / LCP elements with this component.
 */
export function FadeIn({
  children,
  delay = 0,
  duration = 0.7,
  className = '',
}: FadeInProps) {
  return (
    <div
      className={className}
      style={{
        animation: `fade-in-up ${duration}s ${delay}s cubic-bezier(0.25,0.1,0.25,1) both`,
      }}
    >
      {children}
    </div>
  );
}
