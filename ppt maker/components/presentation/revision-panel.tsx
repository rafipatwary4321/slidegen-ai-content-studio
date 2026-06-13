"use client";

import { Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

interface RevisionPanelProps {
  instruction: string;
  onInstructionChange: (value: string) => void;
  onApply: () => void;
  loading?: boolean;
  disabled?: boolean;
}

export function RevisionPanel({
  instruction,
  onInstructionChange,
  onApply,
  loading = false,
  disabled = false
}: RevisionPanelProps) {
  return (
    <section className="panel">
      <h3 className="panel-title">Prompt-Based Revision</h3>
      <p className="panel-subtitle">Refine outline using natural language instructions.</p>
      <textarea
        value={instruction}
        onChange={(event) => onInstructionChange(event.target.value)}
        disabled={disabled}
        placeholder="Make it more investor-friendly"
        className="mt-4 h-24 w-full resize-none rounded-xl border border-white/10 bg-slate-900/70 p-3 text-sm text-slate-100 outline-none ring-violet-400/50 placeholder:text-slate-500 focus:ring-2 disabled:opacity-70"
      />
      <Button className="mt-4" onClick={onApply} disabled={disabled || loading || !instruction.trim()}>
        <Sparkles className="h-4 w-4" />
        {loading ? "Revising..." : "Apply Revision"}
      </Button>
    </section>
  );
}
