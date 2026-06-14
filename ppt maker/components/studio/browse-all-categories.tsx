"use client";

import type { ContentCategory } from "@/lib/content-studio/types";
import { CONTENT_CATEGORIES } from "@/lib/content-studio/categories";
import { MarketplaceCategoryCard } from "@/components/studio/marketplace-category-card";

interface BrowseAllCategoriesProps {
  categories?: ContentCategory[];
  title?: string;
  subtitle?: string;
}

export function BrowseAllCategories({
  categories = CONTENT_CATEGORIES,
  title = "Browse all categories",
  subtitle
}: BrowseAllCategoriesProps) {
  const description =
    subtitle ?? `${categories.length} creative formats — presentations to podcast covers`;

  return (
    <section id="browse-all" className="scroll-mt-8 space-y-6">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 className="text-xl font-semibold text-white sm:text-2xl">{title}</h2>
          <p className="mt-1.5 text-sm text-slate-400">{description}</p>
        </div>
        <span className="inline-flex w-fit items-center rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 text-xs font-medium text-slate-300">
          {categories.length} categories
        </span>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {categories.map((c) => (
          <MarketplaceCategoryCard key={c.id} category={c} />
        ))}
      </div>
    </section>
  );
}
