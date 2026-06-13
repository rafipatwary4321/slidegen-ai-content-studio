"use client";

import { useRouter } from "next/navigation";
import type { Route } from "next";
import { useState } from "react";
import { Search, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { CONTENT_CATEGORIES, searchCategories } from "@/lib/content-studio/categories";
import { useStudioStore } from "@/lib/content-studio/store";

export function UniversalPromptBox() {
  const router = useRouter();
  const [prompt, setPrompt] = useState("");
  const searchQuery = useStudioStore((s) => s.searchQuery);
  const setSearchQuery = useStudioStore((s) => s.setSearchQuery);

  function handleBrowse() {
    const q = prompt.trim() || searchQuery.trim();
    if (!q) {
      router.push("/dashboard/new");
      return;
    }
    const match = searchCategories(q)[0];
    if (match?.legacyRoute) {
      router.push(match.legacyRoute as Route);
      return;
    }
    if (match) {
      router.push(`/dashboard/studio/${match.id}` as Route);
      return;
    }
    router.push("/dashboard/new");
  }

  return (
    <div className="space-y-4">
      <div className="relative">
        <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
        <input
          type="search"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search categories — presentations, Instagram, certificates…"
          className="studio-input py-3.5 pl-11 pr-4"
        />
      </div>
      <div className="flex flex-col gap-3 sm:flex-row">
        <input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleBrowse()}
          placeholder="What do you want to create today?"
          className="studio-input flex-1 py-3.5"
        />
        <Button onClick={handleBrowse} size="lg" className="shrink-0 px-8 sm:min-w-[140px]">
          <Sparkles className="h-4 w-4" /> Browse
        </Button>
      </div>
      <p className="rounded-xl border border-white/5 bg-white/[0.02] px-3 py-2 text-xs leading-relaxed text-slate-400">
        Presentations use the full PPT generator. Other categories open their dedicated generators where available.
      </p>
    </div>
  );
}
