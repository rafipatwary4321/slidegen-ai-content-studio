"use client";

import { Heart } from "lucide-react";
import { CONTENT_CATEGORIES } from "@/lib/content-studio/categories";
import { useStudioStore } from "@/lib/content-studio/store";
import { MarketplaceCategoryCard } from "@/components/studio/marketplace-category-card";

export function FavoritesSection() {
  const ids = useStudioStore((s) => s.favoriteCategoryIds);
  const favorites = CONTENT_CATEGORIES.filter((c) => ids.includes(c.id));

  return (
    <section className="space-y-4">
      <div className="flex items-center gap-2 px-0.5">
        <Heart className="h-4 w-4 fill-pink-400 text-pink-400" />
        <div>
          <h2 className="text-xl font-semibold text-white">Favorites</h2>
          <p className="text-sm text-slate-400">Your pinned categories for quick access</p>
        </div>
      </div>
      {favorites.length ? (
        <div className="studio-scroll-row flex gap-4 overflow-x-auto pb-3">
          {favorites.map((c) => (
            <div key={c.id} className="w-56 shrink-0">
              <MarketplaceCategoryCard category={c} />
            </div>
          ))}
        </div>
      ) : (
        <div className="rounded-2xl border border-dashed border-white/10 bg-white/[0.02] px-6 py-8 text-center">
          <p className="text-sm text-slate-400">Tap the heart on any category to save it here.</p>
        </div>
      )}
    </section>
  );
}
