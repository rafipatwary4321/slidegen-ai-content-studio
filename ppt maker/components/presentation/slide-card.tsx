import { Eye } from "lucide-react";

interface SlideCardProps {
  title: string;
  accent: string;
}

export function SlideCard({ title, accent }: SlideCardProps) {
  return (
    <article className="group overflow-hidden rounded-2xl border border-white/10 bg-slate-900/65 transition hover:-translate-y-0.5 hover:border-white/20 hover:shadow-[0_16px_40px_rgba(2,6,23,0.45)]">
      <div className={`h-24 bg-gradient-to-r ${accent}`} />
      <div className="p-4">
        <div className="flex items-start justify-between gap-3">
          <h4 className="text-sm font-semibold text-white">{title}</h4>
          <span className="rounded-md bg-white/10 p-1 text-slate-300 transition group-hover:bg-white/15 group-hover:text-white">
            <Eye className="h-3.5 w-3.5" />
          </span>
        </div>
        <p className="mt-2 text-xs leading-relaxed text-slate-400">Outline title from your saved deck. Export applies your current theme and bullets.</p>
      </div>
    </article>
  );
}
