"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import type { Route } from "next";
import { ArrowRight, Sparkles, Star } from "lucide-react";
import type { ContentCategory } from "@/lib/content-studio/types";
import { categoryIcon } from "@/lib/content-studio/icons";
import { FEATURED_MARKETPLACE_CATEGORIES, resolveFeaturedCategory } from "@/lib/content-studio/marketplace";

function FeaturedCard({ category }: { category: ContentCategory }) {
  const router = useRouter();
  const Icon = categoryIcon(category.icon);
  const href = category.legacyRoute ?? (`/dashboard/studio/${category.id}` as Route);

  function handleGenerate(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    router.push(href as Route);
  }

  return (
    <Link
      href={href as Route}
      className="marketplace-featured-card group relative flex w-[min(100%,280px)] shrink-0 flex-col overflow-hidden rounded-2xl border border-white/10 bg-slate-900/80 shadow-[0_16px_40px_rgba(2,6,23,0.45)] sm:w-64"
    >
      <div className={`relative h-36 bg-gradient-to-br ${category.gradient} p-5`}>
        <div className="absolute inset-0 bg-black/0 transition duration-300 group-hover:bg-black/20" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent opacity-60" />
        <Icon className="relative h-10 w-10 text-white drop-shadow-lg transition duration-300 group-hover:scale-110" />
        <span className="absolute right-3 top-3 rounded-full border border-white/20 bg-black/40 px-2.5 py-0.5 text-[10px] font-semibold text-white/95 backdrop-blur">
          Featured
        </span>
      </div>
      <div className="flex flex-1 flex-col p-4 sm:p-5">
        <h3 className="text-base font-semibold text-white group-hover:text-cyan-50">{category.name}</h3>
        <p className="mt-2 line-clamp-2 flex-1 text-xs leading-relaxed text-slate-400">{category.description}</p>
        <button
          type="button"
          onClick={handleGenerate}
          className="marketplace-generate-btn mt-4 inline-flex w-full items-center justify-center gap-2 rounded-xl py-2.5 text-xs font-semibold text-white"
        >
          <Sparkles className="h-3.5 w-3.5" /> Open
        </button>
      </div>
    </Link>
  );
}

export function FeaturedCategoriesSection() {
  const featured = FEATURED_MARKETPLACE_CATEGORIES.map(resolveFeaturedCategory).filter(Boolean) as ContentCategory[];

  return (
    <section className="space-y-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="flex h-8 w-8 items-center justify-center rounded-xl border border-amber-400/30 bg-amber-500/10">
              <Star className="h-4 w-4 text-amber-400" />
            </span>
            <div>
              <h2 className="text-xl font-semibold text-white sm:text-2xl">Featured categories</h2>
              <p className="mt-0.5 text-sm text-slate-400">Most popular formats to start creating instantly</p>
            </div>
          </div>
        </div>
        <a
          href="#browse-all"
          className="inline-flex w-fit items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-xs font-medium text-cyan-300 transition hover:border-cyan-400/30 hover:bg-cyan-500/10 hover:text-cyan-200"
        >
          View all <ArrowRight className="h-3.5 w-3.5" />
        </a>
      </div>
      <div className="studio-scroll-row -mx-1 flex gap-4 overflow-x-auto px-1 pb-3 pt-1">
        {featured.map((c) => (
          <FeaturedCard key={c.id} category={c} />
        ))}
      </div>
    </section>
  );
}
