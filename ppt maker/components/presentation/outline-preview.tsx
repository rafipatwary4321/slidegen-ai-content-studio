import { ListChecks } from "lucide-react";

interface OutlinePreviewProps {
  items?: string[];
}

export function OutlinePreview({ items = [] }: OutlinePreviewProps) {
  return (
    <section className="panel">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="panel-title">Outline Preview</h3>
        <span className="inline-flex items-center gap-1 rounded-full border border-white/15 bg-white/5 px-2 py-1 text-[11px] text-slate-300">
          <ListChecks className="h-3 w-3" /> Draft
        </span>
      </div>
      <ol className="space-y-2 text-sm text-slate-300">
        {items.map((item, idx) => (
          <li key={`${item}-${idx}`} className="rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2.5 transition hover:bg-white/[0.06]">
            <span className="mr-2 text-cyan-200">{idx + 1}.</span>{item}
          </li>
        ))}
      </ol>
    </section>
  );
}
