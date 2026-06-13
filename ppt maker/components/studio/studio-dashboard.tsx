"use client";

import { CONTENT_CATEGORIES, searchCategories } from "@/lib/content-studio/categories";
import { useStudioStore } from "@/lib/content-studio/store";
import { MarketplaceHero } from "@/components/studio/marketplace-hero";
import { FeaturedCategoriesSection } from "@/components/studio/featured-categories";
import { BrowseAllCategories } from "@/components/studio/browse-all-categories";

export function StudioDashboard() {
  const searchQuery = useStudioStore((s) => s.searchQuery);
  const filtered = searchQuery.trim() ? searchCategories(searchQuery) : null;

  return (
    <div className="space-y-8 pb-10">
      <MarketplaceHero />
      {filtered ? (
        <BrowseAllCategories categories={filtered} />
      ) : (
        <>
          <FeaturedCategoriesSection />
          <BrowseAllCategories categories={CONTENT_CATEGORIES} />
        </>
      )}
    </div>
  );
}
