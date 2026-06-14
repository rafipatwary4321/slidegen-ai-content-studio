"use client";

import { useEffect, useMemo, useState } from "react";
import { Calendar, MapPin, Megaphone, User } from "lucide-react";
import { PosterExportPngButton } from "@/components/poster/export-png-button";
import { designToneLabel, posterTypeLabel, TONE_PALETTES } from "@/lib/poster/constants";
import type { PosterAiCopyData, PosterData, PosterFormState } from "@/lib/poster/types";

interface PosterPreviewProps {
  form: PosterFormState;
  generated?: PosterData | null;
  aiCopy?: PosterAiCopyData | null;
}

const ASPECT_CLASS: Record<string, string> = {
  "1:1": "aspect-square max-w-md",
  "4:5": "aspect-[4/5] max-w-sm",
  "9:16": "aspect-[9/16] max-w-[280px]",
  A4: "aspect-[210/297] max-w-sm"
};

export function PosterPreview({ form, generated, aiCopy }: PosterPreviewProps) {
  const [logoUrl, setLogoUrl] = useState<string | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  useEffect(() => {
    if (!form.logoFile) {
      setLogoUrl(null);
      return;
    }
    const url = URL.createObjectURL(form.logoFile);
    setLogoUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [form.logoFile]);

  useEffect(() => {
    if (!form.imageFile) {
      setImageUrl(null);
      return;
    }
    const url = URL.createObjectURL(form.imageFile);
    setImageUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [form.imageFile]);

  const palette = TONE_PALETTES[aiCopy?.designTone ?? form.designTone];
  const title = generated?.title ?? aiCopy?.title ?? form.title;
  const subtitle = generated?.subtitle ?? aiCopy?.subtitle ?? form.subtitle;
  const ctaText = aiCopy?.ctaText ?? form.ctaText;
  const typeLabel = posterTypeLabel(generated?.posterType ?? aiCopy?.posterType ?? form.posterType);
  const layoutNote = generated?.layoutInstructions ?? aiCopy?.layoutDirection;
  const activeTone = aiCopy?.designTone ?? form.designTone;

  const headlineFont = form.language === "bn" ? "var(--font-bengali)" : "Georgia, 'Times New Roman', serif";
  const bodyFont = form.language === "bn" ? "var(--font-bengali)" : "Inter, system-ui, sans-serif";
  const isLight = activeTone === "academic-clean";

  const toneLayout = useMemo(() => {
    switch (activeTone) {
      case "bold-political":
        return { titleSize: "clamp(1.35rem, 5vw, 2rem)", accentBar: true };
      case "modern-youth":
        return { titleSize: "clamp(1.3rem, 4.8vw, 1.9rem)", accentBar: true, gradient: true };
      case "luxury-event":
        return { titleSize: "clamp(1.2rem, 4.2vw, 1.75rem)", accentBar: false, goldRule: true };
      case "academic-clean":
        return { titleSize: "clamp(1.15rem, 4vw, 1.6rem)", accentBar: false };
      default:
        return { titleSize: "clamp(1.2rem, 4.2vw, 1.7rem)", accentBar: false };
    }
  }, [activeTone]);

  const aspectClass = ASPECT_CLASS[form.aspectRatio] ?? ASPECT_CLASS.A4;

  return (
    <section className="generator-preview-shell">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="panel-title">Live preview</h3>
          <p className="panel-subtitle">
            {designToneLabel(activeTone)} · {form.aspectRatio}
            {aiCopy ? ` · AI ${aiCopy.source}` : ""}
            {generated ? " · Generated" : ""}
          </p>
        </div>
        <span className="rounded-full border border-violet-400/25 bg-violet-500/10 px-2.5 py-1 text-[10px] font-medium text-violet-200">
          Poster
        </span>
      </div>

      <div className="preview-canvas-frame">
        <div className="flex justify-center">
        <article
          className={`relative flex w-full flex-col overflow-hidden rounded-2xl shadow-2xl ${aspectClass}`}
          style={{ backgroundColor: palette.bg, color: palette.text }}
        >
          {toneLayout.gradient ? (
            <div className="h-3 w-full bg-gradient-to-r from-fuchsia-500 via-violet-500 to-cyan-400 sm:h-4" />
          ) : toneLayout.accentBar ? (
            <div className="h-3 w-full sm:h-4" style={{ backgroundColor: palette.accent }} />
          ) : toneLayout.goldRule ? (
            <div className="mx-5 mt-4 h-px" style={{ backgroundColor: palette.accent }} />
          ) : null}

          <div className="flex flex-1 flex-col px-4 pb-4 pt-4 sm:px-5 sm:pb-5 sm:pt-5">
            <div className="flex items-start justify-between gap-3">
              <span
                className="inline-block rounded px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider"
                style={{ backgroundColor: `${palette.accent}33`, color: palette.accent }}
              >
                {typeLabel}
              </span>
              {logoUrl ? (
                <img src={logoUrl} alt="Logo" className="h-9 w-9 rounded object-contain sm:h-11 sm:w-11" />
              ) : (
                <div
                  className="flex h-9 w-9 items-center justify-center rounded border border-dashed text-[9px] sm:h-11 sm:w-11"
                  style={{ borderColor: `${palette.muted}55`, color: palette.muted }}
                >
                  LOGO
                </div>
              )}
            </div>

            <h2
              className="mt-4 font-bold leading-tight tracking-tight"
              style={{ fontFamily: headlineFont, fontSize: toneLayout.titleSize, color: palette.text }}
            >
              {title || "Your poster title"}
            </h2>

            {subtitle ? (
              <p className="mt-2 text-xs leading-relaxed sm:text-sm" style={{ fontFamily: bodyFont, color: palette.muted }}>
                {subtitle}
              </p>
            ) : null}

            <div
              className="mt-4 flex-1 overflow-hidden rounded-xl border"
              style={{ borderColor: `${palette.muted}33`, backgroundColor: palette.surface, minHeight: 100 }}
            >
              {imageUrl ? (
                <img src={imageUrl} alt="Hero" className="h-full w-full object-cover" style={{ minHeight: 100 }} />
              ) : (
                <div className="flex h-full min-h-[100px] items-center justify-center text-[10px] uppercase tracking-widest" style={{ color: palette.muted }}>
                  Hero image
                </div>
              )}
            </div>

            <div className="mt-4 space-y-1.5 text-xs" style={{ fontFamily: bodyFont, color: palette.muted }}>
              {form.dateTime ? (
                <p className="flex items-center gap-1.5">
                  <Calendar className="h-3.5 w-3.5 shrink-0" style={{ color: palette.accent }} />
                  {form.dateTime}
                </p>
              ) : null}
              {form.venue ? (
                <p className="flex items-center gap-1.5">
                  <MapPin className="h-3.5 w-3.5 shrink-0" style={{ color: palette.accent }} />
                  {form.venue}
                </p>
              ) : null}
              {form.organizer ? (
                <p className="flex items-center gap-1.5">
                  <User className="h-3.5 w-3.5 shrink-0" style={{ color: palette.accent }} />
                  {form.organizer}
                </p>
              ) : null}
            </div>

            <div className="mt-4 flex items-center justify-between gap-3">
              <button
                type="button"
                className="rounded-xl px-4 py-2.5 text-xs font-bold uppercase tracking-wide"
                style={{
                  backgroundColor: palette.cta,
                  color: isLight ? "#ffffff" : palette.bg
                }}
              >
                {ctaText || "Learn More"}
              </button>
              <Megaphone className="h-4 w-4 opacity-40" style={{ color: palette.muted }} />
            </div>
          </div>
        </article>
        </div>
      </div>

      <div className="rounded-xl border border-white/10 bg-slate-950/40 p-3">
        <PosterExportPngButton
          form={form}
          generated={generated}
          aiCopy={aiCopy}
          logoObjectUrl={logoUrl}
          imageObjectUrl={imageUrl}
        />
      </div>

      {layoutNote ? (
        <div className="rounded-xl border border-white/10 bg-slate-950/50 p-3.5">
          <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-500">Layout direction</p>
          <p className="mt-1.5 text-xs leading-relaxed text-slate-400">{layoutNote}</p>
        </div>
      ) : null}
    </section>
  );
}
