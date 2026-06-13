"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ArrowLeft, Download, Redo2, Undo2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ToolsSidebar } from "@/components/studio/editor/tools-sidebar";
import { CanvasStage } from "@/components/studio/editor/canvas-stage";
import { PropertiesPanel } from "@/components/studio/editor/properties-panel";
import { LayersPanel } from "@/components/studio/editor/layers-panel";
import { AiAssistantPanel } from "@/components/studio/editor/ai-assistant-panel";
import { useEditorStore } from "@/lib/content-studio/editor-store";
import { useStudioStore } from "@/lib/content-studio/store";
import { getCategoryById } from "@/lib/content-studio/categories";
import { EXPORT_FORMATS } from "@/lib/content-studio/constants";
import type { ExportFormatId } from "@/lib/content-studio/types";

interface StudioEditorProps {
  projectId: string;
}

export function StudioEditor({ projectId }: StudioEditorProps) {
  const getProject = useStudioStore((s) => s.getProject);
  const saveProject = useStudioStore((s) => s.saveProject);
  const project = useEditorStore((s) => s.project);
  const setProject = useEditorStore((s) => s.setProject);
  const undo = useEditorStore((s) => s.undo);
  const redo = useEditorStore((s) => s.redo);
  const canUndo = useEditorStore((s) => s.canUndo);
  const canRedo = useEditorStore((s) => s.canRedo);
  const [exportMsg, setExportMsg] = useState<string | null>(null);

  useEffect(() => {
    const stored = getProject(projectId);
    if (stored) setProject(stored);
  }, [projectId, getProject, setProject]);

  useEffect(() => {
    if (!project) return;
    saveProject(project);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- persist on layer edits via updatedAt
  }, [project?.updatedAt, project?.id, saveProject]);

  if (!project) {
    return (
      <div className="panel">
        <p className="text-sm text-slate-300">Project not found. Generate a design from the studio first.</p>
        <Link href="/dashboard" className="mt-3 inline-block text-sm text-cyan-300 hover:underline">
          Back to studio
        </Link>
      </div>
    );
  }

  const category = getCategoryById(project.categoryId);
  const exports = category?.supportedExports ?? (["png", "pdf"] as ExportFormatId[]);

  async function handleExport(format: ExportFormatId) {
    if (!project) return;
    setExportMsg(`Preparing ${format.toUpperCase()} export…`);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"}/api/v1/content/export`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_id: project.id, format, layers: project.layers, title: project.title, aspect_ratio: project.aspectRatio })
      });
      if (!res.ok) throw new Error("Export failed");
      const data = await res.json();
      if (data.download_url) {
        window.open(`${process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"}${data.download_url}`, "_blank");
        setExportMsg(`${format.toUpperCase()} ready.`);
      } else {
        setExportMsg(data.message ?? "Export queued.");
      }
    } catch {
      setExportMsg(`Export ${format.toUpperCase()} — use editor screenshot or PPT pipeline for presentations.`);
    }
  }

  return (
    <div className="-mx-2 flex h-[calc(100vh-7rem)] flex-col overflow-hidden rounded-2xl border border-white/10 bg-slate-950/90 sm:-mx-0">
      <header className="flex flex-wrap items-center gap-2 border-b border-white/10 px-4 py-3">
        <Link href="/dashboard" className="inline-flex items-center gap-1 text-xs text-slate-400 hover:text-white">
          <ArrowLeft className="h-3.5 w-3.5" /> Studio
        </Link>
        <span className="text-sm font-medium text-white">{project.title}</span>
        <span className="text-xs text-slate-500">{category?.name}</span>
        <div className="ml-auto flex flex-wrap items-center gap-2">
          <Button size="sm" variant="ghost" onClick={undo} disabled={!canUndo()}>
            <Undo2 className="h-4 w-4" />
          </Button>
          <Button size="sm" variant="ghost" onClick={redo} disabled={!canRedo()}>
            <Redo2 className="h-4 w-4" />
          </Button>
          {exports.map((f) => {
            const label = EXPORT_FORMATS.find((e) => e.id === f)?.label ?? f.toUpperCase();
            return (
              <Button key={f} size="sm" variant="ghost" onClick={() => handleExport(f)}>
                <Download className="h-3.5 w-3.5" /> {label}
              </Button>
            );
          })}
        </div>
      </header>
      {exportMsg ? <p className="border-b border-white/5 px-4 py-1 text-[11px] text-cyan-200/80">{exportMsg}</p> : null}

      <div className="flex min-h-0 flex-1">
        <div className="flex flex-col border-r border-white/10">
          <ToolsSidebar />
          <LayersPanel />
          <AiAssistantPanel />
        </div>
        <CanvasStage />
        <PropertiesPanel />
      </div>
    </div>
  );
}
