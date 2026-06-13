"use client";

import type { StudioProject } from "@/lib/content-studio/types";
import { ASPECT_RATIOS } from "@/lib/content-studio/constants";

interface DesignPreviewProps {
  project: StudioProject;
  scale?: number;
  className?: string;
}

export function DesignPreview({ project, scale = 0.12, className = "" }: DesignPreviewProps) {
  const dims = ASPECT_RATIOS.find((a) => a.id === project.aspectRatio) ?? ASPECT_RATIOS[2];
  const sorted = [...project.layers].sort((a, b) => a.zIndex - b.zIndex);

  return (
    <div
      className={`relative overflow-hidden rounded-xl bg-slate-950 ring-1 ring-white/10 ${className}`}
      style={{ width: dims.width * scale, height: dims.height * scale }}
    >
      {sorted.map((layer) =>
        layer.visible ? (
          <div
            key={layer.id}
            className="absolute overflow-hidden"
            style={{
              left: layer.x * scale,
              top: layer.y * scale,
              width: layer.width * scale,
              height: layer.height * scale,
              opacity: layer.opacity,
              zIndex: layer.zIndex,
              backgroundColor: layer.type === "shape" ? layer.fill ?? "#8B5CF6" : "transparent",
              color: "#fff",
              fontSize: Math.max(6, 12 * scale),
              padding: layer.type === "text" ? 2 : 0
            }}
          >
            {layer.type === "text" ? layer.content : null}
          </div>
        ) : null
      )}
    </div>
  );
}
