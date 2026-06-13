"use client";

import { useCallback, useRef, useState } from "react";
import type { CanvasLayer } from "@/lib/content-studio/types";
import { ASPECT_RATIOS } from "@/lib/content-studio/constants";
import { useEditorStore } from "@/lib/content-studio/editor-store";

interface CanvasStageProps {
  scale?: number;
}

export function CanvasStage({ scale = 0.45 }: CanvasStageProps) {
  const project = useEditorStore((s) => s.project);
  const selectedLayerId = useEditorStore((s) => s.selectedLayerId);
  const selectLayer = useEditorStore((s) => s.selectLayer);
  const updateLayer = useEditorStore((s) => s.updateLayer);
  const pushHistory = useEditorStore((s) => s.pushHistory);

  const dragRef = useRef<{ id: string; startX: number; startY: number; layerX: number; layerY: number } | null>(null);
  const [draggingId, setDraggingId] = useState<string | null>(null);

  const onMove = useCallback(
    (e: MouseEvent) => {
      const d = dragRef.current;
      if (!d || !project) return;
      const ratio = 1 / scale;
      updateLayer(d.id, {
        x: d.layerX + (e.clientX - d.startX) * ratio,
        y: d.layerY + (e.clientY - d.startY) * ratio
      }, { history: false });
    },
    [project, scale, updateLayer]
  );

  const onUp = useCallback(() => {
    dragRef.current = null;
    setDraggingId(null);
    window.removeEventListener("mousemove", onMove);
    window.removeEventListener("mouseup", onUp);
  }, [onMove]);

  if (!project) return null;

  const dims = ASPECT_RATIOS.find((a) => a.id === project.aspectRatio) ?? ASPECT_RATIOS[2];
  const sorted = [...project.layers].sort((a, b) => a.zIndex - b.zIndex);

  function startDrag(e: React.MouseEvent, layer: CanvasLayer) {
    if (layer.locked) return;
    e.stopPropagation();
    pushHistory();
    selectLayer(layer.id);
    dragRef.current = { id: layer.id, startX: e.clientX, startY: e.clientY, layerX: layer.x, layerY: layer.y };
    setDraggingId(layer.id);
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onUp);
  }

  return (
    <div className="flex flex-1 items-center justify-center overflow-auto bg-slate-900/50 p-6">
      <div
        className="relative overflow-hidden rounded-lg shadow-2xl ring-1 ring-white/10"
        style={{
          width: dims.width * scale,
          height: dims.height * scale,
          background: "#0f172a"
        }}
        onClick={() => selectLayer(null)}
      >
        {sorted.map((layer) =>
          layer.visible ? (
            <div
              key={layer.id}
              role="presentation"
              onMouseDown={(e) => startDrag(e, layer)}
              className={`absolute cursor-move select-none ${
                selectedLayerId === layer.id ? "ring-2 ring-cyan-400" : ""
              } ${draggingId === layer.id ? "opacity-90" : ""}`}
              style={{
                left: layer.x * scale,
                top: layer.y * scale,
                width: layer.width * scale,
                height: layer.height * scale,
                opacity: layer.opacity,
                transform: `rotate(${layer.rotation}deg)`,
                zIndex: layer.zIndex,
                backgroundColor: layer.type === "shape" ? layer.fill ?? "#8B5CF6" : "transparent",
                color: "#fff",
                fontSize: Math.max(10, 14 * scale),
                padding: layer.type === "text" ? 4 * scale : 0,
                overflow: "hidden"
              }}
            >
              {layer.type === "text" ? layer.content : null}
            </div>
          ) : null
        )}
      </div>
    </div>
  );
}
