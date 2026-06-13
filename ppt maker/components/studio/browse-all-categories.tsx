"use client";

import type { ContentCategory } from "@/lib/content-studio/types";
import { CONTENT_CATEGORIES } from "@/lib/content-studio/categories";
import { MarketplaceCategoryCard } from "@/components/studio/marketplace-category-card";

interface BrowseAllCategoriesProps {
  categories?: ContentCategory[];
}

export function BrowseAllCategories({ categories = CONTENT_CATEGORIES }: BrowseAllCategoriesProps) {
  return (
    <section id="browse-all" className="scroll-mt-6 space-y-5">
      <div>
        <h2 className="text-xl font-semibold text-white">Browse all categories</h2>
        <p className="mt-1 text-sm text-slate-400">{categories.length} creative formats — presentations to podcast covers</p>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {categories.map((c) => (
          <MarketplaceCategoryCard key={c.id} category={c} />
        ))}
      </div>
    </section>
  );
}
