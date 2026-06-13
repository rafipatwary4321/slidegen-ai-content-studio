import type { StudioTemplate } from "@/lib/content-studio/types";

export const FEATURED_TEMPLATES: StudioTemplate[] = [
  { id: "pitch-deck-pro", categoryId: "presentations", title: "Investor Pitch Pro", subtitle: "16:9 deck", aspectRatio: "16:9", featured: true, gradient: "from-violet-600 to-indigo-500" },
  { id: "news-flash", categoryId: "breaking-news-cards", title: "Breaking Flash", subtitle: "Alert layout", aspectRatio: "16:9", featured: true, gradient: "from-red-600 to-orange-500" },
  { id: "ig-launch", categoryId: "instagram-posts", title: "Product Launch", subtitle: "Square feed", aspectRatio: "1:1", featured: true, gradient: "from-pink-500 to-orange-400" },
  { id: "yt-clickbait-clean", categoryId: "youtube-thumbnails", title: "Bold Thumbnail", subtitle: "High contrast", aspectRatio: "16:9", featured: true, gradient: "from-red-600 to-rose-500" },
  { id: "event-summit", categoryId: "event-posters", title: "Summit Poster", subtitle: "Print ready", aspectRatio: "A4", featured: true, gradient: "from-fuchsia-600 to-purple-500" },
  { id: "infographic-stats", categoryId: "infographics", title: "Stats Story", subtitle: "Data viz", aspectRatio: "4:5", featured: true, gradient: "from-cyan-500 to-emerald-500" },
  { id: "resume-modern", categoryId: "resume-builder", title: "Modern CV", subtitle: "A4 layout", aspectRatio: "A4", featured: true, gradient: "from-slate-600 to-cyan-500" },
  { id: "podcast-neon", categoryId: "podcast-covers", title: "Neon Podcast", subtitle: "Square art", aspectRatio: "1:1", featured: true, gradient: "from-purple-700 to-indigo-500" },
  { id: "restaurant-special", categoryId: "restaurant-marketing", title: "Chef Special", subtitle: "Menu promo", aspectRatio: "1:1", featured: true, gradient: "from-orange-500 to-red-600" },
  { id: "real-estate-lux", categoryId: "real-estate-templates", title: "Luxury Listing", subtitle: "Property card", aspectRatio: "16:9", featured: true, gradient: "from-sky-600 to-blue-500" }
];

export function templatesForCategory(categoryId: string): StudioTemplate[] {
  return FEATURED_TEMPLATES.filter((t) => t.categoryId === categoryId);
}

export function getTemplateById(id: string): StudioTemplate | undefined {
  return FEATURED_TEMPLATES.find((t) => t.id === id);
}
