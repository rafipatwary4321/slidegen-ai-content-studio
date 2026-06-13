"use client";

import { UniversalPromptBox } from "@/components/studio/universal-prompt-box";

export function MarketplaceHero() {
  return (
    <section className="panel bg-gradient-to-br from-violet-600/20 via-slate-900/40 to-cyan-500/15 p-6 sm:p-8">
      <p className="text-xs uppercase tracking-[0.2em] text-cyan-200/80">Category Marketplace</p>
      <h1 className="mt-2 text-2xl font-semibold text-white sm:text-3xl">What do you want to create?</h1>
      <p className="mt-2 max-w-2xl text-sm text-slate-300">
        Browse 25+ formats or jump straight into the presentation generator.
      </p>
      <div className="mt-6">
        <UniversalPromptBox />
      </div>
    </section>
  );
}
