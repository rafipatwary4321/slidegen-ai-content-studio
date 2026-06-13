"use client";

import { X } from "lucide-react";
import { CONTENT_CATEGORIES } from "@/lib/content-studio/categories";
import { categoryIcon } from "@/lib/content-studio/icons";

interface CategoryPickerModalProps {
  open: boolean;
  onClose: () => void;
  onSelect: (categoryId: string) => void;
  title?: string;
}

export function CategoryPickerModal({ open, onClose, onSelect, title = "Choose a category" }: CategoryPickerModalProps) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/70 p-4 backdrop-blur-sm sm:items-center">
      <div className="max-h-[85vh] w-full max-w-4xl overflow-hidden rounded-2xl border border-white/15 bg-slate-950 shadow-2xl">
        <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
          <div>
            <h2 className="text-lg font-semibold text-white">{title}</h2>
            <p className="text-sm text-slate-400">We couldn&apos;t confidently detect the right format.</p>
          </div>
          <button type="button" onClick={onClose} className="rounded-lg p-2 text-slate-400 hover:bg-white/10 hover:text-white">
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="grid max-h-[calc(85vh-5rem)] grid-cols-1 gap-2 overflow-y-auto p-4 sm:grid-cols-2">
          {CONTENT_CATEGORIES.map((c) => {
            const Icon = categoryIcon(c.icon);
            return (
              <button
                key={c.id}
                type="button"
                onClick={() => onSelect(c.id)}
                className="flex items-center gap-3 rounded-xl border border-white/10 bg-white/[0.03] p-3 text-left transition hover:border-cyan-300/35 hover:bg-white/[0.06]"
              >
                <span className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br ${c.gradient}`}>
                  <Icon className="h-5 w-5 text-white" />
                </span>
                <span className="min-w-0">
                  <span className="block text-sm font-semibold text-white">{c.name}</span>
                  <span className="block truncate text-xs text-slate-400">{c.description}</span>
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
