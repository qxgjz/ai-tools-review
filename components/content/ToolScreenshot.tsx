"use client";

import { useState } from "react";
import { Image as ImageIcon, ZoomIn, X } from "lucide-react";

interface ToolScreenshotProps {
  toolSlug: string;
  toolName: string;
  vendor?: string;
  className?: string;
}

export function ToolScreenshot({ toolSlug, toolName, vendor, className = "" }: ToolScreenshotProps) {
  const [isLightboxOpen, setIsLightboxOpen] = useState(false);
  const [imageError, setImageError] = useState(false);

  const screenshotUrl = `/screenshots/${toolSlug}.svg`;

  if (imageError) {
    return (
      <div className={`rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 p-8 text-center ${className}`}>
        <ImageIcon className="w-12 h-12 mx-auto text-gray-400 mb-3" />
        <p className="text-gray-500 dark:text-gray-400 text-sm">Screenshot coming soon</p>
        <p className="text-gray-400 dark:text-gray-500 text-xs mt-1">We're working on capturing {toolName} screenshots</p>
      </div>
    );
  }

  return (
    <>
      <div className={`relative group cursor-pointer rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-all ${className}`}
        onClick={() => setIsLightboxOpen(true)}
      >
        <img
          src={screenshotUrl}
          alt={`${toolName} screenshot - ${vendor || "AIToolCrux"}`}
          className="w-full h-auto object-cover"
          onError={() => setImageError(true)}
          loading="lazy"
        />
        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors flex items-center justify-center opacity-0 group-hover:opacity-100">
          <div className="bg-white/90 dark:bg-gray-800/90 rounded-full p-3 shadow-lg">
            <ZoomIn className="w-5 h-5 text-gray-700 dark:text-gray-300" />
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-3 opacity-0 group-hover:opacity-100 transition-opacity">
          <p className="text-white text-sm font-medium">Click to enlarge</p>
        </div>
      </div>

      {/* Lightbox */}
      {isLightboxOpen && (
        <div
          className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4"
          onClick={() => setIsLightboxOpen(false)}
        >
          <button
            className="absolute top-4 right-4 text-white/80 hover:text-white transition-colors"
            onClick={() => setIsLightboxOpen(false)}
          >
            <X className="w-8 h-8" />
          </button>
          <img
            src={screenshotUrl}
            alt={`${toolName} screenshot - ${vendor || "AIToolCrux"}`}
            className="max-w-full max-h-[90vh] object-contain rounded-lg shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          />
        </div>
      )}
    </>
  );
}
