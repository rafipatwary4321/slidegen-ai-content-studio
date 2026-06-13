"use client";

import Link from "next/link";
import type { Route } from "next";
import { Clock, Sparkles } from "lucide-react";
import { useStudioStore } from "@/lib/content-studio/store";
import { getCategoryById } from "@/lib/content-studio/categories";
import { categoryIcon } from "@/lib/content-studio/icons";

export function RecentProjectsSection() {
  const recent = useStudioStore((s) => s.recentProjects);

  return (
    <section className="space-y-4">
      <div className="flex items-center gap-2 px-0.5">
        <Clock className="h-4 w-4 text-slate-400" />
        <div>
          <h2 className="text-xl font-semibold text-white">Recent projects</h2>
          <p className="text-sm text-slate-400">Pick up where you left off</p>
        </div>
      </div>
      {recent.length ? (
        <div className="studio-scroll-row flex gap-4 overflow-x-auto pb-3">
          {recent.map((p) => {
            const cat = getCategoryById(p.categoryId);
            const Icon = cat ? categoryIcon(cat.icon) : Sparkles;
            return (
              <Link
                key={p.id}
                href={`/dashboard/studio/editor/${p.id}` as Route}
                className="marketplace-recent-card group w-56 shrink-0 overflow-hidden rounded-2xl border border-white/10 bg-slate-900/60"
              >
                <div className={`h-20 bg-gradient-to-br ${cat?.gradient ?? "from-slate-600 to-slate-800"} p-4`}>
                  <Icon className="h-6 w-6 text-white/90 transition group-hover:scale-105" />
                </div>
                <div className="p-3.5">
                  <p className="truncate text-sm font-semibold text-white">{p.title}</p>
                  <p className="mt-1 text-[11px] text-slate-400">{cat?.name ?? p.categoryId}</p>
                  <p className="mt-2 text-[10px] text-slate-500">{new Date(p.createdAt).toLocaleDateString()}</p>
                </div>
              </Link>
            );
          })}
        </div>
      ) : (
        <div className="rounded-2xl border border-dashed border-white/10 bg-white/[0.02] px-6 py-10 text-center">
          <p className="text-sm text-slate-400">No projects yet — generate your first design above.</p>
        </div>
      )}
    </section>
  );
}
