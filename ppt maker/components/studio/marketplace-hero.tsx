"use client";

import { LayoutGrid, Sparkles, Wand2 } from "lucide-react";
import { UniversalPromptBox } from "@/components/studio/universal-prompt-box";

const statPills = [
  { icon: LayoutGrid, label: "25+ formats" },
  { icon: Sparkles, label: "AI-powered copy" },
  { icon: Wand2, label: "One-click generators" }
] as const;

export function MarketplaceHero() {
  return (
    <section className="marketplace-hero panel relative overflow-hidden bg-gradient-to-br from-violet-600/25 via-slate-900/50 to-cyan-500/20 p-6 sm:p-8 lg:p-10">
      <div className="pointer-events-none absolute -right-16 -top-16 h-56 w-56 rounded-full bg-violet-500/25 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-20 left-1/3 h-48 w-48 rounded-full bg-cyan-400/15 blur-3xl" />

      <div className="relative">
        <p className="inline-flex items-center gap-2 rounded-full border border-cyan-400/30 bg-cyan-500/10 px-3 py-1 text-[11px] font-medium uppercase tracking-[0.18em] text-cyan-100">
          <Sparkles className="h-3.5 w-3.5" />
          AI Content Studio
        </p>
        <h1 className="mt-4 text-3xl font-semibold tracking-tight text-white sm:text-4xl">What do you want to create?</h1>
        <p className="mt-3 max-w-2xl text-sm leading-relaxed text-slate-300 sm:text-base">
          Browse 25+ creative formats or jump straight into presentations, news photocards, and posters.
        </p>

        <div className="mt-5 flex flex-wrap gap-2">
          {statPills.map(({ icon: Icon, label }) => (
            <span
              key={label}
              className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.05] px-3 py-1 text-xs text-slate-300"
            >
              <Icon className="h-3.5 w-3.5 text-cyan-300" />
              {label}
            </span>
          ))}
        </div>

        <div className="mt-7">
          <UniversalPromptBox />
        </div>
      </div>
    </section>
  );
}
