"use client";

import { Eye, EyeOff, GripVertical } from "lucide-react";
import { useEditorStore } from "@/lib/content-studio/editor-store";

export function LayersPanel() {
  const project = useEditorStore((s) => s.project);
  const selectedLayerId = useEditorStore((s) => s.selectedLayerId);
  const selectLayer = useEditorStore((s) => s.selectLayer);
  const updateLayer = useEditorStore((s) => s.updateLayer);

  if (!project) return null;

  const layers = [...project.layers].sort((a, b) => b.zIndex - a.zIndex);

  return (
    <div className="border-b border-white/10 px-3 py-2">
      <p className="mb-2 text-[11px] font-medium uppercase tracking-wide text-slate-400">Layers</p>
      <ul className="max-h-36 space-y-1 overflow-y-auto">
        {layers.map((layer) => (
          <li key={layer.id}>
            <button
              type="button"
              onClick={() => selectLayer(layer.id)}
              className={`flex w-full items-center gap-2 rounded-lg px-2 py-1.5 text-left text-xs ${
                selectedLayerId === layer.id ? "bg-cyan-400/15 text-cyan-100" : "text-slate-300 hover:bg-white/5"
              }`}
            >
              <GripVertical className="h-3 w-3 shrink-0 text-slate-500" />
              <span className="flex-1 truncate">{layer.name}</span>
              <span
                role="button"
                tabIndex={0}
                onClick={(e) => {
                  e.stopPropagation();
                  updateLayer(layer.id, { visible: !layer.visible });
                }}
                onKeyDown={() => {}}
                className="text-slate-400"
              >
                {layer.visible ? <Eye className="h-3.5 w-3.5" /> : <EyeOff className="h-3.5 w-3.5" />}
              </span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
