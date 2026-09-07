"use client";

import { useEffect, useRef, useState } from "react";
import { motion, useScroll, useTransform } from "framer-motion";

interface MarqueeProps {
  images: string[];
  direction?: "left" | "right";
  speed?: number;
  className?: string;
}

export function Marquee({
  images,
  direction = "left",
  speed = 0.3,
  className = "",
}: MarqueeProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [sectionTop, setSectionTop] = useState(0);

  useEffect(() => {
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      setSectionTop(rect.top + window.scrollY);
    }
  }, []);

  const { scrollY } = useScroll();
  const offset = useTransform(
    scrollY,
    [sectionTop - window.innerHeight, sectionTop + 1000],
    [0, 1000]
  );

  const tripledImages = [...images, ...images, ...images];

  return (
    <div
      ref={containerRef}
      className={`overflow-hidden ${className}`}
      style={{ willChange: "transform" }}
    >
      <motion.div
        className="flex gap-3"
        style={{
          x: direction === "left"
            ? useTransform(offset, (v) => -(v * speed))
            : useTransform(offset, (v) => v * speed),
        }}
      >
        {tripledImages.map((src, i) => (
          <div
            key={i}
            className="flex-shrink-0 w-[420px] h-[270px] rounded-2xl overflow-hidden"
          >
            <img
              src={src}
              alt={`Marquee image ${i + 1}`}
              className="w-full h-full object-cover"
              loading="lazy"
            />
          </div>
        ))}
      </motion.div>
    </div>
  );
}

interface LogoMarqueeProps {
  logos: { name: string; icon: string; color: string }[];
  direction?: "left" | "right";
  className?: string;
}

export function LogoMarquee({
  logos,
  direction = "left",
  className = "",
}: LogoMarqueeProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    let animationId: number;
    let lastTime = 0;

    const animate = (time: number) => {
      if (lastTime !== 0) {
        const delta = time - lastTime;
        setOffset((prev) => {
          const newOffset = direction === "left"
            ? prev + delta * 0.05
            : prev - delta * 0.05;
          return newOffset;
        });
      }
      lastTime = time;
      animationId = requestAnimationFrame(animate);
    };

    animationId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationId);
  }, [direction]);

  const tripledLogos = [...logos, ...logos, ...logos];

  return (
    <div
      ref={containerRef}
      className={`overflow-hidden py-8 ${className}`}
      style={{ willChange: "transform" }}
    >
      <div
        className="flex gap-6 items-center"
        style={{
          transform: `translateX(${-(offset % (logos.length * 180))}px)`,
        }}
      >
        {tripledLogos.map((logo, i) => (
          <div
            key={i}
            className="flex-shrink-0 flex items-center gap-3 px-6 py-4 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 hover:bg-white/10 transition-colors duration-300"
          >
            <div
              className={`w-10 h-10 rounded-lg bg-gradient-to-br ${logo.color} flex items-center justify-center text-white font-bold text-lg`}
            >
              {logo.name.charAt(0)}
            </div>
            <span className="text-white/80 font-medium whitespace-nowrap">
              {logo.name}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
