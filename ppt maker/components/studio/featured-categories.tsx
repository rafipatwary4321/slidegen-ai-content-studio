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
      className="marketplace-featured-card group relative flex w-[min(100%,280px)] shrink-0 flex-col overflow-hidden rounded-2xl border border-white/10 bg-slate-900/70 sm:w-64"
    >
      <div className={`relative h-36 bg-gradient-to-br ${category.gradient} p-5`}>
        <div className="absolute inset-0 bg-black/0 transition duration-300 group-hover:bg-black/15" />
        <Icon className="relative h-10 w-10 text-white drop-shadow-lg transition duration-300 group-hover:scale-110" />
        <span className="absolute right-3 top-3 rounded-full bg-black/35 px-2 py-0.5 text-[10px] font-medium text-white/90 backdrop-blur">
          Featured
        </span>
      </div>
      <div className="flex flex-1 flex-col p-4">
        <h3 className="text-base font-semibold text-white">{category.name}</h3>
        <p className="mt-1.5 line-clamp-2 flex-1 text-xs leading-relaxed text-slate-400">{category.description}</p>
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
    <section className="space-y-4">
      <div className="flex items-end justify-between gap-3 px-0.5">
        <div>
          <div className="flex items-center gap-2">
            <Star className="h-4 w-4 text-amber-400" />
            <h2 className="text-xl font-semibold text-white">Featured categories</h2>
          </div>
          <p className="mt-1 text-sm text-slate-400">Most popular formats to start creating instantly</p>
        </div>
        <a href="#browse-all" className="hidden items-center gap-1 text-xs text-cyan-300 transition hover:text-cyan-200 sm:inline-flex">
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
