"use client";

import Link from "next/link";
import type { Route } from "next";
import { Flame, Sparkles } from "lucide-react";
import type { StudioTemplate } from "@/lib/content-studio/types";
import { FEATURED_TEMPLATES, getTemplateById } from "@/lib/content-studio/templates";
import { TRENDING_TEMPLATE_IDS } from "@/lib/content-studio/marketplace";
import { getCategoryById } from "@/lib/content-studio/categories";

export function TrendingTemplatesSection() {
  const trending = TRENDING_TEMPLATE_IDS.map((id) => getTemplateById(id)).filter((t): t is StudioTemplate => !!t);
  const templates = trending.length ? trending : FEATURED_TEMPLATES.slice(0, 8);

  return (
    <section className="space-y-4">
      <div className="flex items-center gap-2 px-0.5">
        <Flame className="h-4 w-4 text-orange-400" />
        <div>
          <h2 className="text-xl font-semibold text-white">Trending templates</h2>
          <p className="text-sm text-slate-400">High-performing starting points across top categories</p>
        </div>
      </div>
      <div className="studio-scroll-row flex gap-4 overflow-x-auto pb-3">
        {templates.map((t) => {
          const category = getCategoryById(t.categoryId);
          const href = `/dashboard/studio/${t.categoryId}?template=${t.id}&prompt=${encodeURIComponent(t.subtitle)}` as Route;
          return (
            <Link
              key={t.id}
              href={href}
              className="marketplace-template-card group w-60 shrink-0 overflow-hidden rounded-2xl border border-white/10 bg-slate-900/60"
            >
              <div className={`relative h-36 bg-gradient-to-br ${t.gradient} p-4`}>
                <div className="absolute inset-0 bg-black/0 transition duration-300 group-hover:bg-black/15" />
                <span className="relative rounded-full bg-black/40 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-white/95 backdrop-blur">
                  Trending
                </span>
              </div>
              <div className="p-4">
                <p className="text-sm font-semibold text-white">{t.title}</p>
                <p className="mt-1 text-xs text-slate-400">{t.subtitle}</p>
                <p className="mt-3 inline-flex items-center gap-1.5 text-[11px] font-medium text-cyan-200/90">
                  <Sparkles className="h-3 w-3" /> {category?.name ?? t.categoryId}
                </p>
              </div>
            </Link>
          );
        })}
      </div>
    </section>
  );
}
