'use client';

import type { ReactNode } from 'react';

interface StackingCardProps {
  children: ReactNode;
  index: number;
  totalCards: number;
  className?: string;
}

export function StackingCard({ children, index, totalCards, className = '' }: StackingCardProps) {
  const targetScale = 1 - (totalCards - 1 - index) * 0.03;

  return (
    <div
      className="h-[85vh] sticky top-24 md:top-32 flex items-start justify-center"
      style={{ zIndex: index + 10 }}
    >
      <div
        className={`w-full max-w-6xl ${className}`}
        style={{
          transform: `scale(${targetScale})`,
          top: `${index * 28}px`,
          position: 'relative',
        }}
      >
        {children}
      </div>
    </div>
  );
}

interface StackingCardsContainerProps {
  children: ReactNode;
  className?: string;
}

export function StackingCardsContainer({ children, className = '' }: StackingCardsContainerProps) {
  return <div className={`relative ${className}`}>{children}</div>;
}
