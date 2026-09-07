"use client";

import { motion } from "framer-motion";
import type { ReactNode } from "react";

interface GradientTextProps {
  children: ReactNode;
  className?: string;
  from?: string;
  to?: string;
}

export function GradientText({
  children,
  className = "",
  from = "#646973",
  to = "#BBCCD7",
}: GradientTextProps) {
  return (
    <span
      className={`bg-clip-text text-transparent ${className}`}
      style={{
        backgroundImage: `linear-gradient(180deg, ${from} 0%, ${to} 100%)`,
        WebkitBackgroundClip: "text",
        WebkitTextFillColor: "transparent",
      }}
    >
      {children}
    </span>
  );
}

interface GradientButtonProps {
  children: ReactNode;
  href?: string;
  onClick?: () => void;
  className?: string;
  type?: "button" | "submit";
}

export function GradientButton({
  children,
  href,
  onClick,
  className = "",
  type = "button",
}: GradientButtonProps) {
  const baseStyle = {
    background:
      "linear-gradient(123deg, #18011F 7%, #B600A8 37%, #7621B0 72%, #BE4C00 100%)",
    boxShadow:
      "0px 4px 4px rgba(181, 1, 167, 0.25), 4px 4px 12px #7721B1 inset",
    outline: "2px solid white",
    outlineOffset: "-3px",
  };

  const classes = `inline-flex items-center gap-2 px-8 py-3 sm:px-10 sm:py-3.5 md:px-12 md:py-4 text-white text-xs sm:text-sm md:text-base font-medium uppercase tracking-widest rounded-full transition-all duration-300 hover:scale-105 hover:shadow-lg ${className}`;

  if (href) {
    return (
      <motion.a
        href={href}
        className={classes}
        style={baseStyle}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.98 }}
      >
        {children}
      </motion.a>
    );
  }

  return (
    <motion.button
      type={type}
      onClick={onClick}
      className={classes}
      style={baseStyle}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.98 }}
    >
      {children}
    </motion.button>
  );
}
