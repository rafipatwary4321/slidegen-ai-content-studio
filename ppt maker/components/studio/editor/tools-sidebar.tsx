"use client";

import { Layers, MousePointer2, Shapes, Type } from "lucide-react";
import { useEditorStore } from "@/lib/content-studio/editor-store";

const tools = [
  { id: "select", icon: MousePointer2, label: "Select" },
  { id: "text", icon: Type, label: "Text" },
  { id: "shape", icon: Shapes, label: "Shape" },
  { id: "layers", icon: Layers, label: "Layers" }
] as const;

export function ToolsSidebar() {
  const project = useEditorStore((s) => s.project);
  const pushHistory = useEditorStore((s) => s.pushHistory);
  const setProject = useEditorStore((s) => s.setProject);

  function addTextLayer() {
    if (!project) return;
    pushHistory();
    const layer = {
      id: crypto.randomUUID(),
      type: "text" as const,
      name: "New text",
      x: 120,
      y: 120,
      width: 400,
      height: 80,
      rotation: 0,
      opacity: 1,
      visible: true,
      locked: false,
      content: "Double-click to edit",
      zIndex: project.layers.length
    };
    setProject({ ...project, layers: [...project.layers, layer], updatedAt: new Date().toISOString() });
  }

  function addShapeLayer() {
    if (!project) return;
    pushHistory();
    const layer = {
      id: crypto.randomUUID(),
      type: "shape" as const,
      name: "New shape",
      x: 200,
      y: 200,
      width: 300,
      height: 200,
      rotation: 0,
      opacity: 1,
      visible: true,
      locked: false,
      fill: "#22D3EE",
      zIndex: project.layers.length
    };
    setProject({ ...project, layers: [...project.layers, layer], updatedAt: new Date().toISOString() });
  }

  return (
    <aside className="flex w-14 flex-col items-center gap-2 border-r border-white/10 bg-slate-950/80 py-4">
      {tools.map((t) => (
        <button
          key={t.id}
          type="button"
          title={t.label}
          onClick={() => {
            if (t.id === "text") addTextLayer();
            if (t.id === "shape") addShapeLayer();
          }}
          className="rounded-xl p-2.5 text-slate-400 transition hover:bg-white/10 hover:text-white"
        >
          <t.icon className="h-5 w-5" />
        </button>
      ))}
    </aside>
  );
}
