"use client";

import { useEffect, useMemo, useState } from "react";
import { Newspaper } from "lucide-react";
import { ExportPngButton } from "@/components/news-photocard/export-png-button";
import { PREVIEW_PALETTES, toneLabel } from "@/lib/news-photocard/constants";
import {
  formatPhotocardDate,
  resolveCategory,
  resolveHeadline,
  resolveSubheadline
} from "@/lib/news-photocard/render-model";
import type { NewsPhotocardAiCopyData, NewsPhotocardData, NewsPhotocardFormState } from "@/lib/news-photocard/types";

interface NewsPhotocardPreviewProps {
  form: NewsPhotocardFormState;
  generated?: NewsPhotocardData | null;
  aiCopy?: NewsPhotocardAiCopyData | null;
}

const ASPECT_CLASS: Record<string, string> = {
  "1:1": "aspect-square max-w-md",
  "4:5": "aspect-[4/5] max-w-sm",
  "9:16": "aspect-[9/16] max-w-[280px]"
};

export function NewsPhotocardPreview({ form, generated, aiCopy }: NewsPhotocardPreviewProps) {
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

  const palette = PREVIEW_PALETTES[form.designStyle];
  const headline = resolveHeadline(form, generated, aiCopy);
  const subheadline = resolveSubheadline(form, generated, aiCopy);
  const category = resolveCategory(form, generated, aiCopy);
  const dateStr = formatPhotocardDate(form.language);
  const layoutNote = generated?.layoutInstructions ?? aiCopy?.layoutDirection;

  const headlineFont = form.language === "bn" ? "var(--font-bengali)" : "Georgia, 'Times New Roman', serif";
  const bodyFont = form.language === "bn" ? "var(--font-bengali)" : "Inter, system-ui, sans-serif";

  const toneStyles = useMemo(() => {
    switch (form.tone) {
      case "breaking-news":
        return { headlineSize: "clamp(1.25rem, 4.5vw, 1.75rem)", strip: true, badgeRadius: "4px" };
      case "premium-editorial":
        return { headlineSize: "clamp(1.15rem, 4vw, 1.6rem)", strip: false, badgeRadius: "2px" };
      case "youth-media":
        return { headlineSize: "clamp(1.3rem, 4.8vw, 1.85rem)", strip: true, badgeRadius: "999px" };
      case "corporate-press":
        return { headlineSize: "clamp(1.1rem, 3.8vw, 1.5rem)", strip: false, badgeRadius: "6px" };
      default:
        return { headlineSize: "clamp(1.2rem, 4vw, 1.65rem)", strip: true, badgeRadius: "4px" };
    }
  }, [form.tone]);

  const aspectClass = ASPECT_CLASS[form.aspectRatio] ?? ASPECT_CLASS["4:5"];

  return (
    <section className="generator-preview-shell">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="panel-title">Live preview</h3>
          <p className="panel-subtitle">
            {toneLabel(aiCopy?.tone ?? form.tone)} · {form.aspectRatio}
            {aiCopy ? ` · AI ${aiCopy.source}` : ""}
            {generated ? " · Generated" : ""}
          </p>
        </div>
        <span className="rounded-full border border-cyan-400/25 bg-cyan-500/10 px-2.5 py-1 text-[10px] font-medium text-cyan-200">
          News
        </span>
      </div>

      <div className="preview-canvas-frame">
        <div className="flex justify-center">
        <article
          className={`relative w-full overflow-hidden rounded-2xl shadow-2xl ${aspectClass}`}
          style={{ backgroundColor: palette.bg, color: palette.text }}
        >
          {toneStyles.strip ? (
            <div className="h-2 w-full sm:h-3" style={{ backgroundColor: palette.accent }} />
          ) : (
            <div className="mx-5 mt-4 h-px" style={{ backgroundColor: palette.gold }} />
          )}

          <div className="flex items-start justify-between gap-3 px-4 pt-4 sm:px-5 sm:pt-5">
            <span
              className="inline-block px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider sm:text-[11px]"
              style={{
                backgroundColor: palette.badge,
                color: palette.text,
                borderRadius: toneStyles.badgeRadius
              }}
            >
              {category}
            </span>

            {logoUrl ? (
              <img src={logoUrl} alt="Logo" className="h-8 w-8 rounded object-contain sm:h-10 sm:w-10" />
            ) : (
              <div
                className="flex h-8 w-8 items-center justify-center rounded border border-dashed sm:h-10 sm:w-10"
                style={{ borderColor: `${palette.muted}55`, color: palette.muted }}
              >
                <Newspaper className="h-4 w-4" />
              </div>
            )}
          </div>

          <div className="px-4 pb-4 pt-3 sm:px-5 sm:pb-5">
            <h2
              className="font-bold leading-tight tracking-tight"
              style={{
                fontFamily: headlineFont,
                fontSize: toneStyles.headlineSize,
                color: palette.text
              }}
            >
              {headline || "Your headline appears here"}
            </h2>

            {subheadline ? (
              <p
                className="mt-2.5 text-xs leading-relaxed sm:text-sm"
                style={{ fontFamily: bodyFont, color: palette.muted }}
              >
                {subheadline}
              </p>
            ) : null}

            <div
              className="mt-4 overflow-hidden rounded-lg border"
              style={{
                borderColor: `${palette.muted}33`,
                backgroundColor: palette.surface,
                minHeight: form.aspectRatio === "9:16" ? "28%" : "22%"
              }}
            >
              {imageUrl ? (
                <img src={imageUrl} alt="Hero" className="h-full w-full object-cover" style={{ minHeight: 120 }} />
              ) : (
                <div
                  className="flex h-full min-h-[100px] items-center justify-center text-[10px] uppercase tracking-widest sm:min-h-[120px]"
                  style={{ color: palette.muted }}
                >
                  Hero image
                </div>
              )}
            </div>

            <div className="mt-4 flex items-center justify-between gap-2 border-t pt-3" style={{ borderColor: `${palette.muted}33` }}>
              <span className="text-[10px] font-medium sm:text-xs" style={{ fontFamily: bodyFont, color: palette.gold }}>
                {dateStr}
              </span>
              <span className="text-[10px] uppercase tracking-wider" style={{ color: palette.muted }}>
                SlideGen News
              </span>
            </div>
          </div>
        </article>
        </div>
      </div>

      <div className="rounded-xl border border-white/10 bg-slate-950/40 p-3">
        <ExportPngButton
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
