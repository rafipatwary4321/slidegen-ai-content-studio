"use client";

import { create } from "zustand";
import type { CanvasLayer, StudioProject } from "@/lib/content-studio/types";

interface EditorSnapshot {
  layers: CanvasLayer[];
}

interface EditorState {
  project: StudioProject | null;
  selectedLayerId: string | null;
  past: EditorSnapshot[];
  future: EditorSnapshot[];
  setProject: (project: StudioProject) => void;
  selectLayer: (id: string | null) => void;
  updateLayer: (id: string, patch: Partial<CanvasLayer>, options?: { history?: boolean }) => void;
  pushHistory: () => void;
  undo: () => void;
  redo: () => void;
  canUndo: () => boolean;
  canRedo: () => boolean;
}

function cloneLayers(layers: CanvasLayer[]): CanvasLayer[] {
  return layers.map((l) => ({ ...l }));
}

export const useEditorStore = create<EditorState>((set, get) => ({
  project: null,
  selectedLayerId: null,
  past: [],
  future: [],
  setProject: (project) => set({ project, selectedLayerId: project.layers[0]?.id ?? null, past: [], future: [] }),
  selectLayer: (id) => set({ selectedLayerId: id }),
  updateLayer: (id, patch, options) => {
    const p = get().project;
    if (!p) return;
    if (options?.history !== false) get().pushHistory();
    set({
      project: {
        ...p,
        layers: p.layers.map((l) => (l.id === id ? { ...l, ...patch } : l)),
        updatedAt: new Date().toISOString()
      }
    });
  },
  pushHistory: () => {
    const p = get().project;
    if (!p) return;
    set({
      past: [...get().past, { layers: cloneLayers(p.layers) }].slice(-30),
      future: []
    });
  },
  undo: () => {
    const { past, project, future } = get();
    if (!project || !past.length) return;
    const prev = past[past.length - 1];
    set({
      past: past.slice(0, -1),
      future: [{ layers: cloneLayers(project.layers) }, ...future],
      project: { ...project, layers: cloneLayers(prev.layers) }
    });
  },
  redo: () => {
    const { future, project, past } = get();
    if (!project || !future.length) return;
    const next = future[0];
    set({
      future: future.slice(1),
      past: [...past, { layers: cloneLayers(project.layers) }],
      project: { ...project, layers: cloneLayers(next.layers) }
    });
  },
  canUndo: () => get().past.length > 0,
  canRedo: () => get().future.length > 0
}));
