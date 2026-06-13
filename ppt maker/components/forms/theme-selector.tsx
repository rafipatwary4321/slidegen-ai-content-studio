"use client";
import { Theme } from "@/lib/api/types";
import { THEMES } from "@/lib/presentation-options";

interface ThemeSelectorProps {
  value?: Theme;
  onChange?: (theme: Theme) => void;
  disabled?: boolean;
}

export function ThemeSelector({ value = "Cinematic Dark", onChange, disabled = false }: ThemeSelectorProps) {
  return (
    <section className="panel">
      <h3 className="panel-title">Theme</h3>
      <p className="panel-subtitle">Apply visual style to all generated slides.</p>
      <div className="mt-4 space-y-2">
        {THEMES.map((theme) => {
          const active = theme === value;
          return (
            <button
              key={theme}
              type="button"
              disabled={disabled}
              onClick={() => onChange?.(theme as Theme)}
              className={`w-full rounded-xl border px-3 py-2.5 text-left text-xs font-medium transition ${
                active
                  ? "border-violet-300/50 bg-violet-400/10 text-violet-100"
                  : "border-white/10 bg-white/[0.03] text-slate-300 hover:border-white/20 hover:bg-white/[0.07]"
              } disabled:cursor-not-allowed disabled:opacity-60`}
            >
              {theme}
            </button>
          );
        })}
      </div>
    </section>
  );
}

