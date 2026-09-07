"use client";

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";

interface AnimatedTextProps {
  text: string;
  className?: string;
  startOpacity?: number;
  endOpacity?: number;
}

export function AnimatedText({
  text,
  className = "",
  startOpacity = 0.2,
  endOpacity = 1,
}: AnimatedTextProps) {
  const containerRef = useRef<HTMLParagraphElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start 0.8", "end 0.2"],
  });

  const characters = text.split("");

  return (
    <p ref={containerRef} className={`relative ${className}`}>
      {characters.map((char, i) => {
        const start = i / characters.length;
        const end = (i + 1) / characters.length;
        const opacity = useTransform(
          scrollYProgress,
          [start, end],
          [startOpacity, endOpacity]
        );

        return (
          <span key={i} className="relative inline-block">
            <span className="invisible">{char}</span>
            <motion.span
              className="absolute inset-0"
              style={{ opacity }}
            >
              {char}
            </motion.span>
          </span>
        );
      })}
    </p>
  );
}
