"use client";
import { Persona } from "@/lib/api/types";
import { PERSONAS } from "@/lib/presentation-options";

interface PersonaSelectorProps {
  value?: Persona;
  onChange?: (persona: Persona) => void;
  disabled?: boolean;
}

export function PersonaSelector({ value = "Business", onChange, disabled = false }: PersonaSelectorProps) {
  return (
    <section className="panel">
      <h3 className="panel-title">Persona</h3>
      <p className="panel-subtitle">Choose audience style and communication tone.</p>
      <div className="mt-4 grid grid-cols-2 gap-2">
        {PERSONAS.map((persona) => {
          const active = persona === value;
          return (
            <button
              key={persona}
              type="button"
              disabled={disabled}
              onClick={() => onChange?.(persona as Persona)}
              className={`rounded-xl border px-3 py-2.5 text-left text-xs font-medium transition ${
                active
                  ? "border-cyan-300/60 bg-cyan-400/10 text-cyan-100"
                  : "border-white/10 bg-white/[0.03] text-slate-300 hover:border-white/20 hover:bg-white/[0.07]"
              } disabled:cursor-not-allowed disabled:opacity-60`}
            >
              {persona}
            </button>
          );
        })}
      </div>
    </section>
  );
}

