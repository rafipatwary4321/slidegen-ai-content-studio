"use client";

import { useRef } from "react";
import { ImagePlus, Sparkles, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  NEWS_ASPECT_RATIOS,
  NEWS_CATEGORIES,
  NEWS_DESIGN_STYLES,
  NEWS_LANGUAGES,
  NEWS_TONES
} from "@/lib/news-photocard/constants";
import type { NewsPhotocardFormState } from "@/lib/news-photocard/types";

interface NewsPhotocardFormProps {
  value: NewsPhotocardFormState;
  onChange: (next: NewsPhotocardFormState) => void;
  onGenerate: () => void;
  onAiCopy?: () => void;
  loading?: boolean;
  aiLoading?: boolean;
  disabled?: boolean;
}

function fieldClass(active = false) {
  return `w-full rounded-xl border bg-slate-950/40 px-3 py-2.5 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-cyan-400/50 ${
    active ? "border-cyan-300/40" : "border-white/10"
  }`;
}

function optionButtonClass(active: boolean) {
  return `rounded-xl border px-3 py-2 text-left text-xs font-medium transition ${
    active
      ? "border-cyan-300/60 bg-cyan-400/10 text-cyan-100"
      : "border-white/10 bg-white/[0.03] text-slate-300 hover:border-white/20 hover:bg-white/[0.07]"
  }`;
}

export function NewsPhotocardForm({
  value,
  onChange,
  onGenerate,
  onAiCopy,
  loading = false,
  aiLoading = false,
  disabled = false
}: NewsPhotocardFormProps) {
  const logoRef = useRef<HTMLInputElement>(null);
  const imageRef = useRef<HTMLInputElement>(null);

  function patch(partial: Partial<NewsPhotocardFormState>) {
    onChange({ ...value, ...partial });
  }

  return (
    <div className="space-y-5">
      <section className="panel">
        <h3 className="panel-title">Headline & copy</h3>
        <p className="panel-subtitle">Primary news text shown on the photocard.</p>
        <div className="mt-4 space-y-3">
          <div>
            <label className="mb-1.5 block text-xs text-slate-400">Headline</label>
            <input
              className={fieldClass()}
              value={value.headline}
              onChange={(e) => patch({ headline: e.target.value })}
              placeholder="Breaking: Major policy announcement (or use AI prompt below)"
              disabled={disabled}
            />
          </div>
          <div>
            <label className="mb-1.5 block text-xs text-slate-400">Subheadline</label>
            <textarea
              className={`${fieldClass()} min-h-[72px] resize-y`}
              value={value.subheadline}
              onChange={(e) => patch({ subheadline: e.target.value })}
              placeholder="Supporting context or dek line"
              disabled={disabled}
            />
          </div>
        </div>
      </section>

      <section className="panel">
        <h3 className="panel-title">News category</h3>
        <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-3">
          {NEWS_CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              type="button"
              disabled={disabled}
              onClick={() => patch({ newsCategory: cat.id })}
              className={optionButtonClass(value.newsCategory === cat.id)}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </section>

      <section className="panel">
        <h3 className="panel-title">Language</h3>
        <div className="mt-3 grid grid-cols-2 gap-2">
          {NEWS_LANGUAGES.map((lang) => (
            <button
              key={lang.id}
              type="button"
              disabled={disabled}
              onClick={() => patch({ language: lang.id })}
              className={optionButtonClass(value.language === lang.id)}
            >
              {lang.label}
            </button>
          ))}
        </div>
      </section>

      <section className="panel">
        <h3 className="panel-title">Aspect ratio</h3>
        <div className="mt-3 grid grid-cols-3 gap-2">
          {NEWS_ASPECT_RATIOS.map((ratio) => (
            <button
              key={ratio.id}
              type="button"
              disabled={disabled}
              onClick={() => patch({ aspectRatio: ratio.id })}
              className={optionButtonClass(value.aspectRatio === ratio.id)}
            >
              {ratio.label}
            </button>
          ))}
        </div>
      </section>

      <section className="panel">
        <h3 className="panel-title">Tone</h3>
        <div className="mt-3 grid gap-2 sm:grid-cols-2">
          {NEWS_TONES.map((tone) => (
            <button
              key={tone.id}
              type="button"
              disabled={disabled}
              onClick={() => patch({ tone: tone.id })}
              className={optionButtonClass(value.tone === tone.id)}
            >
              <span className="block font-semibold">{tone.label}</span>
              <span className="mt-0.5 block text-[10px] font-normal text-slate-400">{tone.description}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="panel">
        <h3 className="panel-title">Theme</h3>
        <p className="panel-subtitle">Dark red, black, white, or gold palette.</p>
        <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
          {NEWS_DESIGN_STYLES.map((style) => (
            <button
              key={style.id}
              type="button"
              disabled={disabled}
              onClick={() => patch({ designStyle: style.id })}
              className={`${optionButtonClass(value.designStyle === style.id)} flex items-center gap-2`}
            >
              <span
                className="h-4 w-4 shrink-0 rounded-full border border-white/20"
                style={{ backgroundColor: style.swatch }}
              />
              {style.label}
            </button>
          ))}
        </div>
      </section>

      <section className="panel">
        <h3 className="panel-title">Assets (optional)</h3>
        <div className="mt-3 grid gap-3 sm:grid-cols-2">
          <div className="rounded-xl border border-dashed border-white/15 bg-white/[0.02] p-4">
            <input
              ref={logoRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={(e) => patch({ logoFile: e.target.files?.[0] ?? null })}
            />
            <button
              type="button"
              disabled={disabled}
              onClick={() => logoRef.current?.click()}
              className="flex w-full items-center gap-2 text-left text-xs text-slate-300 hover:text-white"
            >
              <Upload className="h-4 w-4 shrink-0 text-cyan-300" />
              {value.logoFile ? value.logoFile.name : "Upload logo"}
            </button>
          </div>
          <div className="rounded-xl border border-dashed border-white/15 bg-white/[0.02] p-4">
            <input
              ref={imageRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={(e) => patch({ imageFile: e.target.files?.[0] ?? null })}
            />
            <button
              type="button"
              disabled={disabled}
              onClick={() => imageRef.current?.click()}
              className="flex w-full items-center gap-2 text-left text-xs text-slate-300 hover:text-white"
            >
              <ImagePlus className="h-4 w-4 shrink-0 text-cyan-300" />
              {value.imageFile ? value.imageFile.name : "Upload hero image"}
            </button>
          </div>
        </div>
      </section>

      <section className="panel border-violet-400/20 bg-violet-500/5">
        <h3 className="panel-title">AI prompt</h3>
        <p className="panel-subtitle">
          Describe the story in rough words — AI will draft headline, subheadline, category, and tone.
        </p>
        <textarea
          className={`${fieldClass()} mt-3 min-h-[96px] resize-y`}
          value={value.aiPrompt}
          onChange={(e) => patch({ aiPrompt: e.target.value })}
          placeholder="e.g. Bangladesh cricket team wins a close T20 match against India"
          disabled={disabled || aiLoading}
        />
        <Button
          size="sm"
          variant="secondary"
          className="mt-3 w-full"
          onClick={onAiCopy}
          disabled={disabled || aiLoading || !value.aiPrompt.trim() || !onAiCopy}
        >
          <Sparkles className="h-4 w-4" />
          {aiLoading ? "Writing copy…" : "Generate copy with AI"}
        </Button>
      </section>

      <Button
        size="lg"
        className="w-full"
        onClick={onGenerate}
        disabled={disabled || loading || (!value.headline.trim() && !value.aiPrompt.trim())}
      >
        <Sparkles className="h-4 w-4" />
        {loading ? "Generating…" : "Generate photocard"}
      </Button>
    </div>
  );
}
