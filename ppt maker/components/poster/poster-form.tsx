"use client";

import { useRef } from "react";
import {
  AlignLeft,
  Calendar,
  Globe,
  ImagePlus,
  LayoutGrid,
  MapPin,
  Megaphone,
  Sparkles,
  Upload,
  User,
  Volume2
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import {
  POSTER_ASPECT_RATIOS,
  POSTER_DESIGN_TONES,
  POSTER_LANGUAGES,
  POSTER_TYPES
} from "@/lib/poster/constants";
import type { PosterFormState } from "@/lib/poster/types";

interface PosterFormProps {
  value: PosterFormState;
  onChange: (next: PosterFormState) => void;
  onGenerate: () => void;
  onAiCopy?: () => void;
  loading?: boolean;
  aiLoading?: boolean;
  disabled?: boolean;
}

function optionClass(active: boolean) {
  return cn("studio-option", active ? "studio-option-active" : "studio-option-idle");
}

function FormSection({
  icon: Icon,
  title,
  subtitle,
  children,
  accent = false
}: {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  accent?: boolean;
}) {
  return (
    <section className={cn("panel", accent && "studio-section-accent")}>
      <div className="studio-section-header">
        <span className="studio-section-icon">
          <Icon className="h-4 w-4" />
        </span>
        <div className="min-w-0 flex-1">
          <h3 className="panel-title">{title}</h3>
          {subtitle ? <p className="panel-subtitle">{subtitle}</p> : null}
        </div>
      </div>
      <div className="mt-4">{children}</div>
    </section>
  );
}

export function PosterForm({
  value,
  onChange,
  onGenerate,
  onAiCopy,
  loading = false,
  aiLoading = false,
  disabled = false
}: PosterFormProps) {
  const logoRef = useRef<HTMLInputElement>(null);
  const imageRef = useRef<HTMLInputElement>(null);

  function patch(partial: Partial<PosterFormState>) {
    onChange({ ...value, ...partial });
  }

  return (
    <div className="space-y-5">
      <FormSection icon={AlignLeft} title="Poster copy">
        <div className="space-y-3">
          <div>
            <label className="studio-section-label">Poster title</label>
            <input
              className="studio-input"
              value={value.title}
              onChange={(e) => patch({ title: e.target.value })}
              placeholder="Annual Innovation Summit 2026 (or use AI prompt below)"
              disabled={disabled}
            />
          </div>
          <div>
            <label className="studio-section-label">Subtitle</label>
            <textarea
              className="studio-input min-h-[80px] resize-y"
              value={value.subtitle}
              onChange={(e) => patch({ subtitle: e.target.value })}
              placeholder="Supporting tagline or event description"
              disabled={disabled}
            />
          </div>
        </div>
      </FormSection>

      <FormSection icon={Megaphone} title="Poster type">
        <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
          {POSTER_TYPES.map((type) => (
            <button
              key={type.id}
              type="button"
              disabled={disabled}
              onClick={() => patch({ posterType: type.id })}
              className={optionClass(value.posterType === type.id)}
            >
              {type.label}
            </button>
          ))}
        </div>
      </FormSection>

      <FormSection icon={Calendar} title="Event details (optional)">
        <div className="space-y-3">
          <div>
            <label className="studio-section-label flex items-center gap-1.5">
              <Calendar className="h-3.5 w-3.5 text-cyan-300" /> Date / time
            </label>
            <input
              className="studio-input"
              value={value.dateTime}
              onChange={(e) => patch({ dateTime: e.target.value })}
              placeholder="Saturday, 14 June 2026 · 10:00 AM"
              disabled={disabled}
            />
          </div>
          <div>
            <label className="studio-section-label flex items-center gap-1.5">
              <MapPin className="h-3.5 w-3.5 text-cyan-300" /> Venue / location
            </label>
            <input
              className="studio-input"
              value={value.venue}
              onChange={(e) => patch({ venue: e.target.value })}
              placeholder="Grand Convention Hall, Dhaka"
              disabled={disabled}
            />
          </div>
          <div>
            <label className="studio-section-label flex items-center gap-1.5">
              <User className="h-3.5 w-3.5 text-cyan-300" /> Organizer
            </label>
            <input
              className="studio-input"
              value={value.organizer}
              onChange={(e) => patch({ organizer: e.target.value })}
              placeholder="SlideGen Events"
              disabled={disabled}
            />
          </div>
          <div>
            <label className="studio-section-label">Call-to-action text</label>
            <input
              className="studio-input"
              value={value.ctaText}
              onChange={(e) => patch({ ctaText: e.target.value })}
              placeholder="Register Now"
              disabled={disabled}
            />
          </div>
        </div>
      </FormSection>

      <div className="grid gap-5 sm:grid-cols-2">
        <FormSection icon={Globe} title="Language">
          <div className="grid grid-cols-2 gap-2">
            {POSTER_LANGUAGES.map((lang) => (
              <button
                key={lang.id}
                type="button"
                disabled={disabled}
                onClick={() => patch({ language: lang.id })}
                className={optionClass(value.language === lang.id)}
              >
                {lang.label}
              </button>
            ))}
          </div>
        </FormSection>

        <FormSection icon={LayoutGrid} title="Aspect ratio">
          <div className="grid grid-cols-2 gap-2">
            {POSTER_ASPECT_RATIOS.map((ratio) => (
              <button
                key={ratio.id}
                type="button"
                disabled={disabled}
                onClick={() => patch({ aspectRatio: ratio.id })}
                className={optionClass(value.aspectRatio === ratio.id)}
              >
                {ratio.label}
              </button>
            ))}
          </div>
        </FormSection>
      </div>

      <FormSection icon={Volume2} title="Design tone">
        <div className="grid gap-2 sm:grid-cols-2">
          {POSTER_DESIGN_TONES.map((tone) => (
            <button
              key={tone.id}
              type="button"
              disabled={disabled}
              onClick={() => patch({ designTone: tone.id })}
              className={optionClass(value.designTone === tone.id)}
            >
              <span className="block font-semibold">{tone.label}</span>
              <span className="mt-0.5 block text-[10px] font-normal text-slate-400">{tone.description}</span>
            </button>
          ))}
        </div>
      </FormSection>

      <FormSection icon={ImagePlus} title="Assets (optional)">
        <div className="grid gap-3 sm:grid-cols-2">
          <div className="studio-upload-zone">
            <input ref={logoRef} type="file" accept="image/*" className="hidden" onChange={(e) => patch({ logoFile: e.target.files?.[0] ?? null })} />
            <button type="button" disabled={disabled} onClick={() => logoRef.current?.click()} className="flex w-full items-center gap-2.5 text-left text-xs text-slate-300 hover:text-white">
              <Upload className="h-4 w-4 shrink-0 text-cyan-300" />
              <span className="truncate">{value.logoFile ? value.logoFile.name : "Upload logo"}</span>
            </button>
          </div>
          <div className="studio-upload-zone">
            <input ref={imageRef} type="file" accept="image/*" className="hidden" onChange={(e) => patch({ imageFile: e.target.files?.[0] ?? null })} />
            <button type="button" disabled={disabled} onClick={() => imageRef.current?.click()} className="flex w-full items-center gap-2.5 text-left text-xs text-slate-300 hover:text-white">
              <ImagePlus className="h-4 w-4 shrink-0 text-cyan-300" />
              <span className="truncate">{value.imageFile ? value.imageFile.name : "Upload hero image"}</span>
            </button>
          </div>
        </div>
      </FormSection>

      <FormSection
        icon={Sparkles}
        title="AI prompt"
        subtitle="Describe your poster in rough words — AI will draft title, subtitle, CTA, type, and tone."
        accent
      >
        <textarea
          className="studio-input min-h-[100px] resize-y"
          value={value.aiPrompt}
          onChange={(e) => patch({ aiPrompt: e.target.value })}
          placeholder="e.g. Tech startup launch party for young founders in Dhaka"
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
      </FormSection>

      <div className="panel border-violet-400/20 bg-violet-500/5">
        <Button
          size="lg"
          className="w-full"
          onClick={onGenerate}
          disabled={disabled || loading || (!value.title.trim() && !value.aiPrompt.trim())}
        >
          <Sparkles className="h-4 w-4" />
          {loading ? "Generating…" : "Generate poster"}
        </Button>
      </div>
    </div>
  );
}
