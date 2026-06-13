"use client";
import { WandSparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

interface PromptInputProps {
  value?: string;
  onChange?: (value: string) => void;
  onGenerate?: () => void;
  loading?: boolean;
  disabled?: boolean;
}

export function PromptInput({
  value = "Make it more professional",
  onChange,
  onGenerate,
  loading = false,
  disabled = false
}: PromptInputProps) {
  return (
    <section className="panel">
      <label htmlFor="prompt" className="panel-title block">
        Prompt Direction
      </label>
      <p className="panel-subtitle">Fine-tune your generated deck&apos;s voice and structure.</p>
      <textarea
        id="prompt"
        value={value}
        disabled={disabled}
        onChange={(event) => onChange?.(event.target.value)}
        placeholder="Make it more professional"
        className="mt-4 h-28 w-full resize-none rounded-xl border border-white/10 bg-slate-900/70 p-3 text-sm text-slate-100 outline-none ring-violet-400/50 placeholder:text-slate-500 focus:ring-2 disabled:opacity-70"
      />
      <Button className="mt-4 w-full" onClick={onGenerate} disabled={disabled || loading || !onGenerate}>
        <WandSparkles className="h-4 w-4" />
        {loading ? "Generating..." : "Generate Presentation"}
      </Button>
    </section>
  );
}

