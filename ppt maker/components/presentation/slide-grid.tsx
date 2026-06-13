import { ImagePlus } from "lucide-react";
import { SlideCard } from "@/components/presentation/slide-card";
import { EmptyState } from "@/components/ui/empty-state";

const ACCENT_ROTATION = [
  "from-fuchsia-500/70 to-violet-500/50",
  "from-cyan-500/70 to-blue-500/50",
  "from-emerald-500/70 to-teal-500/50",
  "from-amber-500/70 to-orange-500/50",
  "from-rose-500/70 to-pink-500/50",
  "from-indigo-500/70 to-violet-500/50"
] as const;

export type SlidePreviewItem = { id: string; title: string };

interface SlideGridProps {
  showHeader?: boolean;
  /** Real outline titles from the user’s latest saved deck; empty shows guidance only. */
  slides?: SlidePreviewItem[];
}

export function SlideGrid({ showHeader = true, slides = [] }: SlideGridProps) {
  if (!slides.length) {
    return (
      <EmptyState
        title="No slide previews yet"
        description="Save a presentation from New Presentation — outline titles from your most recent deck appear here automatically."
        icon={<ImagePlus className="h-5 w-5" />}
      />
    );
  }

  return (
    <section>
      {showHeader ? (
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-white">Slide preview</h3>
          <span className="text-xs text-slate-400">{slides.length} slides from your outline</span>
        </div>
      ) : null}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {slides.map((slide, index) => (
          <SlideCard
            key={slide.id}
            title={slide.title}
            accent={ACCENT_ROTATION[index % ACCENT_ROTATION.length]}
          />
        ))}
      </div>
    </section>
  );
}
