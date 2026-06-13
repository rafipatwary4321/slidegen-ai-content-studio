import type { ContentCategory } from "@/lib/content-studio/types";
import { getCategoryById } from "@/lib/content-studio/categories";

export interface FeaturedCategoryEntry {
  categoryId: string;
  displayName?: string;
  displayDescription?: string;
}

export const FEATURED_MARKETPLACE_CATEGORIES: FeaturedCategoryEntry[] = [
  { categoryId: "presentations" },
  { categoryId: "news-photocards" },
  { categoryId: "breaking-news-cards", displayName: "Breaking News" },
  { categoryId: "event-posters" },
  {
    categoryId: "instagram-posts",
    displayName: "Social Media Posts",
    displayDescription: "Instagram, Facebook, and feed-ready creatives in seconds."
  },
  { categoryId: "certificates" }
];

export function resolveFeaturedCategory(entry: FeaturedCategoryEntry): ContentCategory | undefined {
  const base = getCategoryById(entry.categoryId);
  if (!base) return undefined;
  return {
    ...base,
    name: entry.displayName ?? base.name,
    description: entry.displayDescription ?? base.description
  };
}

export const TRENDING_TEMPLATE_IDS = [
  "pitch-deck-pro",
  "news-flash",
  "ig-launch",
  "yt-clickbait-clean",
  "event-summit",
  "infographic-stats",
  "resume-modern",
  "podcast-neon"
] as const;
