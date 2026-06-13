"use client";

import { useEditorStore } from "@/lib/content-studio/editor-store";

export function PropertiesPanel() {
  const project = useEditorStore((s) => s.project);
  const selectedLayerId = useEditorStore((s) => s.selectedLayerId);
  const updateLayer = useEditorStore((s) => s.updateLayer);

  const layer = project?.layers.find((l) => l.id === selectedLayerId);

  if (!layer) {
    return (
      <aside className="w-72 shrink-0 border-l border-white/10 bg-slate-950/80 p-4">
        <p className="text-sm font-medium text-white">Properties</p>
        <p className="mt-2 text-xs text-slate-400">Select a layer on the canvas to edit position, content, and style.</p>
      </aside>
    );
  }

  const selected = layer;

  function patch<K extends keyof typeof selected>(key: K, value: (typeof selected)[K]) {
    updateLayer(selected.id, { [key]: value });
  }

  return (
    <aside className="w-72 shrink-0 space-y-4 overflow-y-auto border-l border-white/10 bg-slate-950/80 p-4">
      <div>
        <p className="text-sm font-medium text-white">Properties</p>
        <p className="text-xs text-slate-400">{selected.name}</p>
      </div>

      <label className="block text-xs text-slate-400">
        Name
        <input
          value={selected.name}
          onChange={(e) => patch("name", e.target.value)}
          className="mt-1 w-full rounded-lg border border-white/10 bg-slate-900 px-2 py-1.5 text-sm text-white"
        />
      </label>

      {selected.type === "text" ? (
        <label className="block text-xs text-slate-400">
          Content
          <textarea
            value={selected.content ?? ""}
            onChange={(e) => patch("content", e.target.value)}
            rows={4}
            className="mt-1 w-full rounded-lg border border-white/10 bg-slate-900 px-2 py-1.5 text-sm text-white"
          />
        </label>
      ) : null}

      {selected.type === "shape" ? (
        <label className="block text-xs text-slate-400">
          Fill
          <input
            type="color"
            value={selected.fill ?? "#8B5CF6"}
            onChange={(e) => patch("fill", e.target.value)}
            className="mt-1 h-9 w-full cursor-pointer rounded-lg border border-white/10 bg-slate-900"
          />
        </label>
      ) : null}

      <div className="grid grid-cols-2 gap-2">
        {(["x", "y", "width", "height", "rotation", "opacity"] as const).map((key) => (
          <label key={key} className="block text-xs capitalize text-slate-400">
            {key}
            <input
              type="number"
              step={key === "opacity" ? 0.1 : 1}
              value={selected[key]}
              onChange={(e) => patch(key, Number(e.target.value))}
              className="mt-1 w-full rounded-lg border border-white/10 bg-slate-900 px-2 py-1.5 text-sm text-white"
            />
          </label>
        ))}
      </div>

      <label className="flex items-center gap-2 text-xs text-slate-300">
        <input type="checkbox" checked={selected.visible} onChange={(e) => patch("visible", e.target.checked)} />
        Visible
      </label>
      <label className="flex items-center gap-2 text-xs text-slate-300">
        <input type="checkbox" checked={selected.locked} onChange={(e) => patch("locked", e.target.checked)} />
        Locked
      </label>
    </aside>
  );
}
