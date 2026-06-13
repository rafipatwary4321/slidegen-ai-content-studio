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
    <div className="space-y-3">
      <div className="relative">
        <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
        <input
          type="search"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search categories — presentations, Instagram, certificates…"
          className="w-full rounded-2xl border border-white/15 bg-slate-950/75 py-3.5 pl-11 pr-4 text-sm text-white outline-none placeholder:text-slate-500 focus:ring-2 focus:ring-cyan-400/25"
        />
      </div>
      <div className="flex flex-col gap-3 sm:flex-row">
        <input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleBrowse()}
          placeholder="What do you want to create today?"
          className="flex-1 rounded-2xl border border-white/15 bg-slate-950/75 px-4 py-3.5 text-sm text-white outline-none placeholder:text-slate-500 focus:ring-2 focus:ring-violet-400/25"
        />
        <Button onClick={handleBrowse} size="lg" className="shrink-0 px-8">
          <Sparkles className="h-4 w-4" /> Browse
        </Button>
      </div>
      <p className="text-xs text-slate-400">
        Presentations use the full PPT generator. Other categories are browse-only until studio generation is ready.
      </p>
    </div>
  );
}
