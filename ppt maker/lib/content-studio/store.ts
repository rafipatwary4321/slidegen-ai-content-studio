"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { BrandKit, StudioProject } from "@/lib/content-studio/types";
import { DEFAULT_BRAND_KIT } from "@/lib/content-studio/constants";

interface StudioState {
  searchQuery: string;
  setSearchQuery: (q: string) => void;
  favoriteCategoryIds: string[];
  favoriteTemplateIds: string[];
  toggleFavoriteCategory: (id: string) => void;
  toggleFavoriteTemplate: (id: string) => void;
  recentProjects: StudioProject[];
  projectsById: Record<string, StudioProject>;
  addRecentProject: (project: StudioProject) => void;
  saveProject: (project: StudioProject) => void;
  getProject: (id: string) => StudioProject | undefined;
  brandKit: BrandKit;
  setBrandKit: (kit: Partial<BrandKit>) => void;
}

export const useStudioStore = create<StudioState>()(
  persist(
    (set, get) => ({
      searchQuery: "",
      setSearchQuery: (q) => set({ searchQuery: q }),
      favoriteCategoryIds: ["presentations", "instagram-posts", "youtube-thumbnails"],
      favoriteTemplateIds: [],
      toggleFavoriteCategory: (id) => {
        const cur = get().favoriteCategoryIds;
        set({
          favoriteCategoryIds: cur.includes(id) ? cur.filter((x) => x !== id) : [...cur, id]
        });
      },
      toggleFavoriteTemplate: (id) => {
        const cur = get().favoriteTemplateIds;
        set({
          favoriteTemplateIds: cur.includes(id) ? cur.filter((x) => x !== id) : [...cur, id]
        });
      },
      recentProjects: [],
      projectsById: {},
      addRecentProject: (project) => {
        const cur = get().recentProjects.filter((p) => p.id !== project.id);
        set({
          recentProjects: [project, ...cur].slice(0, 12),
          projectsById: { ...get().projectsById, [project.id]: project }
        });
      },
      saveProject: (project) =>
        set({
          projectsById: { ...get().projectsById, [project.id]: project },
          recentProjects: [project, ...get().recentProjects.filter((p) => p.id !== project.id)].slice(0, 12)
        }),
      getProject: (id) => get().projectsById[id],
      brandKit: DEFAULT_BRAND_KIT,
      setBrandKit: (kit) => set({ brandKit: { ...get().brandKit, ...kit } })
    }),
    { name: "slidegen-studio-v1" }
  )
);
