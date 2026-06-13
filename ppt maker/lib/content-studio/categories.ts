import type { ContentCategory } from "@/lib/content-studio/types";

export const CONTENT_CATEGORIES: ContentCategory[] = [
  {
    id: "presentations",
    name: "Presentations",
    description: "AI slide decks from documents — full PPT export pipeline.",
    icon: "Presentation",
    defaultAspectRatio: "16:9",
    supportedAspectRatios: ["16:9", "4:5", "A4"],
    supportedExports: ["pptx", "pdf", "png", "zip"],
    gradient: "from-violet-600/80 to-indigo-500/60",
    tags: ["slides", "business", "pitch"],
    legacyRoute: "/dashboard/new"
  },
  {
    id: "news-photocards",
    name: "News Photocards",
    description: "Editorial photocards for digital newsrooms.",
    icon: "Newspaper",
    defaultAspectRatio: "4:5",
    supportedAspectRatios: ["1:1", "4:5", "9:16"],
    supportedExports: ["png", "jpg", "pdf"],
    gradient: "from-rose-600/70 to-orange-500/50",
    tags: ["news", "media"],
    legacyRoute: "/dashboard/generate/news-photocard"
  },
  {
    id: "breaking-news-cards",
    name: "Breaking News Cards",
    description: "Urgent alert layouts with bold headlines.",
    icon: "Zap",
    defaultAspectRatio: "16:9",
    supportedAspectRatios: ["16:9", "1:1", "9:16"],
    supportedExports: ["png", "jpg"],
    gradient: "from-red-600/80 to-amber-500/50",
    tags: ["breaking", "alert"]
  },
  {
    id: "event-posters",
    name: "Event Posters",
    description: "Posters for conferences, concerts, and meetups.",
    icon: "Calendar",
    defaultAspectRatio: "A4",
    supportedAspectRatios: ["A4", "4:5", "16:9"],
    supportedExports: ["png", "pdf", "jpg"],
    gradient: "from-fuchsia-600/70 to-purple-500/50",
    tags: ["events"],
    legacyRoute: "/dashboard/generate/poster?type=event"
  },
  {
    id: "facebook-posts",
    name: "Facebook Posts",
    description: "Feed posts optimized for engagement.",
    icon: "Share2",
    defaultAspectRatio: "1:1",
    supportedAspectRatios: ["1:1", "4:5", "16:9"],
    supportedExports: ["png", "jpg"],
    gradient: "from-blue-600/70 to-cyan-500/50",
    tags: ["social", "facebook"]
  },
  {
    id: "instagram-posts",
    name: "Instagram Posts",
    description: "Square and portrait feed creatives.",
    icon: "Instagram",
    defaultAspectRatio: "1:1",
    supportedAspectRatios: ["1:1", "4:5"],
    supportedExports: ["png", "jpg"],
    gradient: "from-pink-600/70 to-orange-500/50",
    tags: ["social", "instagram"]
  },
  {
    id: "instagram-stories",
    name: "Instagram Stories",
    description: "Vertical story frames with CTAs.",
    icon: "Smartphone",
    defaultAspectRatio: "9:16",
    supportedAspectRatios: ["9:16"],
    supportedExports: ["png", "jpg"],
    gradient: "from-purple-600/70 to-pink-500/50",
    tags: ["stories"]
  },
  {
    id: "facebook-covers",
    name: "Facebook Covers",
    description: "Page cover banners that crop safely.",
    icon: "Layout",
    defaultAspectRatio: "16:9",
    supportedAspectRatios: ["16:9"],
    supportedExports: ["png", "jpg"],
    gradient: "from-blue-700/70 to-indigo-500/50",
    tags: ["covers"]
  },
  {
    id: "youtube-thumbnails",
    name: "YouTube Thumbnails",
    description: "Click-worthy thumbnail compositions.",
    icon: "Youtube",
    defaultAspectRatio: "16:9",
    supportedAspectRatios: ["16:9"],
    supportedExports: ["png", "jpg"],
    gradient: "from-red-600/80 to-rose-500/50",
    tags: ["youtube", "video"]
  },
  {
    id: "youtube-community-posts",
    name: "YouTube Community Posts",
    description: "Community tab announcements and polls.",
    icon: "MessageSquare",
    defaultAspectRatio: "1:1",
    supportedAspectRatios: ["1:1", "16:9"],
    supportedExports: ["png", "jpg"],
    gradient: "from-red-500/60 to-violet-500/50",
    tags: ["youtube"]
  },
  {
    id: "political-posters",
    name: "Political Posters",
    description: "Campaign visuals with clear messaging.",
    icon: "Landmark",
    defaultAspectRatio: "A4",
    supportedAspectRatios: ["A4", "4:5", "16:9"],
    supportedExports: ["png", "pdf"],
    gradient: "from-slate-600/80 to-blue-600/50",
    tags: ["political"],
    legacyRoute: "/dashboard/generate/poster?type=political"
  },
  {
    id: "educational-posters",
    name: "Educational Posters",
    description: "Classroom and campus informational posters.",
    icon: "GraduationCap",
    defaultAspectRatio: "A4",
    supportedAspectRatios: ["A4", "16:9"],
    supportedExports: ["png", "pdf"],
    gradient: "from-emerald-600/70 to-teal-500/50",
    tags: ["education"],
    legacyRoute: "/dashboard/generate/poster?type=educational"
  },
  {
    id: "certificates",
    name: "Certificates",
    description: "Award and completion certificates.",
    icon: "Award",
    defaultAspectRatio: "A4",
    supportedAspectRatios: ["A4", "16:9"],
    supportedExports: ["png", "pdf"],
    gradient: "from-amber-600/70 to-yellow-500/40",
    tags: ["certificates"]
  },
  {
    id: "id-cards",
    name: "ID Cards",
    description: "Employee and membership ID layouts.",
    icon: "CreditCard",
    defaultAspectRatio: "16:9",
    supportedAspectRatios: ["16:9", "4:5"],
    supportedExports: ["png", "pdf"],
    gradient: "from-cyan-600/70 to-blue-500/50",
    tags: ["id"]
  },
  {
    id: "flyers",
    name: "Flyers",
    description: "Promotional flyers for print and digital.",
    icon: "FileImage",
    defaultAspectRatio: "A4",
    supportedAspectRatios: ["A4", "4:5"],
    supportedExports: ["png", "pdf", "jpg"],
    gradient: "from-orange-600/70 to-red-500/50",
    tags: ["flyers"],
    legacyRoute: "/dashboard/generate/poster?type=business"
  },
  {
    id: "brochures",
    name: "Brochures",
    description: "Multi-panel brochure concepts.",
    icon: "BookOpen",
    defaultAspectRatio: "A4",
    supportedAspectRatios: ["A4", "16:9"],
    supportedExports: ["pdf", "png"],
    gradient: "from-indigo-600/70 to-violet-500/50",
    tags: ["brochures"]
  },
  {
    id: "infographics",
    name: "Infographics",
    description: "Data storytelling with charts and icons.",
    icon: "BarChart3",
    defaultAspectRatio: "4:5",
    supportedAspectRatios: ["4:5", "16:9", "A4"],
    supportedExports: ["png", "pdf", "jpg"],
    gradient: "from-cyan-600/70 to-emerald-500/50",
    tags: ["data", "charts"]
  },
  {
    id: "resume-builder",
    name: "Resume Builder",
    description: "Professional CV and resume layouts.",
    icon: "Briefcase",
    defaultAspectRatio: "A4",
    supportedAspectRatios: ["A4"],
    supportedExports: ["pdf", "png"],
    gradient: "from-slate-500/70 to-cyan-500/50",
    tags: ["resume", "career"]
  },
  {
    id: "invitation-cards",
    name: "Invitation Cards",
    description: "Weddings, parties, and formal invites.",
    icon: "Heart",
    defaultAspectRatio: "4:5",
    supportedAspectRatios: ["4:5", "A4", "1:1"],
    supportedExports: ["png", "pdf", "jpg"],
    gradient: "from-pink-500/70 to-rose-400/50",
    tags: ["invites"]
  },
  {
    id: "ad-creatives",
    name: "Ad Creatives",
    description: "Performance ads for paid campaigns.",
    icon: "Megaphone",
    defaultAspectRatio: "1:1",
    supportedAspectRatios: ["1:1", "4:5", "9:16", "16:9"],
    supportedExports: ["png", "jpg", "zip"],
    gradient: "from-violet-600/80 to-fuchsia-500/50",
    tags: ["ads"]
  },
  {
    id: "product-promotions",
    name: "Product Promotions",
    description: "Product launch and sale creatives.",
    icon: "ShoppingBag",
    defaultAspectRatio: "1:1",
    supportedAspectRatios: ["1:1", "4:5", "16:9"],
    supportedExports: ["png", "jpg", "pdf"],
    gradient: "from-emerald-500/70 to-lime-500/50",
    tags: ["ecommerce"],
    legacyRoute: "/dashboard/generate/poster?type=product"
  },
  {
    id: "ngo-campaign-materials",
    name: "NGO Campaign Materials",
    description: "Awareness and fundraising visuals.",
    icon: "HandHeart",
    defaultAspectRatio: "4:5",
    supportedAspectRatios: ["4:5", "16:9", "A4"],
    supportedExports: ["png", "pdf", "jpg"],
    gradient: "from-teal-600/70 to-green-500/50",
    tags: ["ngo"],
    legacyRoute: "/dashboard/generate/poster?type=awareness"
  },
  {
    id: "real-estate-templates",
    name: "Real Estate Templates",
    description: "Listings, open houses, and agent promos.",
    icon: "Home",
    defaultAspectRatio: "16:9",
    supportedAspectRatios: ["16:9", "4:5", "1:1"],
    supportedExports: ["png", "pdf", "jpg"],
    gradient: "from-sky-600/70 to-blue-500/50",
    tags: ["real-estate"]
  },
  {
    id: "restaurant-marketing",
    name: "Restaurant Marketing",
    description: "Menus, promos, and delivery graphics.",
    icon: "UtensilsCrossed",
    defaultAspectRatio: "1:1",
    supportedAspectRatios: ["1:1", "4:5", "9:16", "A4"],
    supportedExports: ["png", "jpg", "pdf"],
    gradient: "from-orange-500/70 to-red-600/50",
    tags: ["food"]
  },
  {
    id: "podcast-covers",
    name: "Podcast Covers",
    description: "Show artwork for Spotify and Apple Podcasts.",
    icon: "Mic",
    defaultAspectRatio: "1:1",
    supportedAspectRatios: ["1:1", "16:9"],
    supportedExports: ["png", "jpg"],
    gradient: "from-purple-700/80 to-indigo-500/50",
    tags: ["podcast", "audio"]
  }
];

export function getCategoryById(id: string): ContentCategory | undefined {
  return CONTENT_CATEGORIES.find((c) => c.id === id);
}

export function searchCategories(query: string): ContentCategory[] {
  const q = query.trim().toLowerCase();
  if (!q) return CONTENT_CATEGORIES;
  return CONTENT_CATEGORIES.filter(
    (c) =>
      c.name.toLowerCase().includes(q) ||
      c.description.toLowerCase().includes(q) ||
      c.tags.some((t) => t.includes(q))
  );
}
