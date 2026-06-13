"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import type { Route } from "next";
import { Heart, Sparkles } from "lucide-react";
import type { ContentCategory } from "@/lib/content-studio/types";
import { categoryIcon } from "@/lib/content-studio/icons";
import { useStudioStore } from "@/lib/content-studio/store";

interface MarketplaceCategoryCardProps {
  category: ContentCategory;
}

export function MarketplaceCategoryCard({ category }: MarketplaceCategoryCardProps) {
  const router = useRouter();
  const Icon = categoryIcon(category.icon);
  const toggleFavorite = useStudioStore((s) => s.toggleFavoriteCategory);
  const isFavorite = useStudioStore((s) => s.favoriteCategoryIds.includes(category.id));
  const href = category.legacyRoute ?? (`/dashboard/studio/${category.id}` as Route);

  function handleGenerate(e: React.MouseEvent) {
    e.preventDefault();
    router.push(href as Route);
  }

  return (
    <article className="marketplace-grid-card group relative flex flex-col overflow-hidden rounded-2xl border border-white/10 bg-slate-900/50">
      <Link href={href as Route} className="block flex-1">
        <div className={`relative h-32 bg-gradient-to-br ${category.gradient} p-5 sm:h-36`}>
          <div className="absolute inset-0 bg-black/0 transition duration-300 group-hover:bg-black/10" />
          <Icon className="relative h-9 w-9 text-white/95 drop-shadow transition duration-300 group-hover:scale-105" />
        </div>
        <div className="p-4 pb-3">
          <h3 className="text-sm font-semibold text-white sm:text-base">{category.name}</h3>
          <p className="mt-1.5 line-clamp-2 text-xs leading-relaxed text-slate-400">{category.description}</p>
        </div>
      </Link>
      <div className="px-4 pb-4">
        <button
          type="button"
          onClick={handleGenerate}
          className="marketplace-generate-btn inline-flex w-full items-center justify-center gap-2 rounded-xl py-2.5 text-xs font-semibold text-white"
        >
          <Sparkles className="h-3.5 w-3.5" /> Open
        </button>
      </div>
      <button
        type="button"
        aria-label={isFavorite ? "Remove from favorites" : "Add to favorites"}
        onClick={() => toggleFavorite(category.id)}
        className="absolute right-3 top-3 rounded-full bg-black/45 p-2 text-white/80 backdrop-blur transition hover:bg-black/65 hover:scale-105"
      >
        <Heart className={`h-3.5 w-3.5 ${isFavorite ? "fill-pink-400 text-pink-400" : ""}`} />
      </button>
    </article>
  );
}
