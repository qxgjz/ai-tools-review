"use client";

import { useRef, type ReactNode } from "react";
import { motion, useScroll, useTransform } from "framer-motion";

interface StackingCardProps {
  children: ReactNode;
  index: number;
  totalCards: number;
  className?: string;
}

export function StackingCard({
  children,
  index,
  totalCards,
  className = "",
}: StackingCardProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const targetScale = 1 - (totalCards - 1 - index) * 0.03;

  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"],
  });

  const scale = useTransform(
    scrollYProgress,
    [0, 0.5, 1],
    [targetScale, targetScale, Math.max(0.9, targetScale - 0.05)]
  );

  return (
    <div
      ref={containerRef}
      className="h-[85vh] sticky top-24 md:top-32 flex items-start justify-center"
      style={{ zIndex: index + 10 }}
    >
      <motion.div
        className={`w-full max-w-6xl ${className}`}
        style={{
          scale,
          top: `${index * 28}px`,
          position: "relative",
        }}
      >
        {children}
      </motion.div>
    </div>
  );
}

interface StackingCardsContainerProps {
  children: ReactNode;
  className?: string;
}

export function StackingCardsContainer({
  children,
  className = "",
}: StackingCardsContainerProps) {
  return (
    <div className={`relative ${className}`}>
      {children}
    </div>
  );
}
