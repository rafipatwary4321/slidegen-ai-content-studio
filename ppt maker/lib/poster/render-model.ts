import { posterTypeLabel, TONE_PALETTES } from "@/lib/poster/constants";
import type {
  PosterAiCopyData,
  PosterAspectRatioId,
  PosterData,
  PosterDesignToneId,
  PosterFormState,
  PosterLanguageId
} from "@/lib/poster/types";

export type PosterPalette = (typeof TONE_PALETTES)[PosterDesignToneId];

export interface PosterRenderModel {
  title: string;
  subtitle: string;
  posterTypeLabel: string;
  dateTime: string;
  venue: string;
  organizer: string;
  ctaText: string;
  aspectRatio: PosterAspectRatioId;
  designTone: PosterDesignToneId;
  language: PosterLanguageId;
  palette: PosterPalette;
  logoObjectUrl: string | null;
  imageObjectUrl: string | null;
}

export const EXPORT_DIMENSIONS: Record<PosterAspectRatioId, { width: number; height: number }> = {
  "1:1": { width: 1080, height: 1080 },
  "4:5": { width: 1080, height: 1350 },
  "9:16": { width: 1080, height: 1920 },
  A4: { width: 1080, height: 1527 }
};

export function resolveTitle(
  form: PosterFormState,
  generated?: PosterData | null,
  aiCopy?: PosterAiCopyData | null
): string {
  return generated?.title ?? aiCopy?.title ?? form.title;
}

export function resolveSubtitle(
  form: PosterFormState,
  generated?: PosterData | null,
  aiCopy?: PosterAiCopyData | null
): string {
  return generated?.subtitle ?? aiCopy?.subtitle ?? form.subtitle;
}

export function resolveCtaText(form: PosterFormState, aiCopy?: PosterAiCopyData | null): string {
  return aiCopy?.ctaText ?? form.ctaText;
}

export function resolveDesignTone(
  form: PosterFormState,
  generated?: PosterData | null,
  aiCopy?: PosterAiCopyData | null
): PosterDesignToneId {
  return generated?.designTone ?? aiCopy?.designTone ?? form.designTone;
}

export function resolvePosterType(
  form: PosterFormState,
  generated?: PosterData | null,
  aiCopy?: PosterAiCopyData | null
) {
  return generated?.posterType ?? aiCopy?.posterType ?? form.posterType;
}

export function buildPosterRenderModel(
  form: PosterFormState,
  options?: {
    generated?: PosterData | null;
    aiCopy?: PosterAiCopyData | null;
    logoObjectUrl?: string | null;
    imageObjectUrl?: string | null;
  }
): PosterRenderModel {
  const designTone = resolveDesignTone(form, options?.generated, options?.aiCopy);
  return {
    title: resolveTitle(form, options?.generated, options?.aiCopy),
    subtitle: resolveSubtitle(form, options?.generated, options?.aiCopy),
    posterTypeLabel: posterTypeLabel(resolvePosterType(form, options?.generated, options?.aiCopy)),
    dateTime: form.dateTime.trim(),
    venue: form.venue.trim(),
    organizer: form.organizer.trim(),
    ctaText: resolveCtaText(form, options?.aiCopy),
    aspectRatio: form.aspectRatio,
    designTone,
    language: form.language,
    palette: TONE_PALETTES[designTone],
    logoObjectUrl: options?.logoObjectUrl ?? null,
    imageObjectUrl: options?.imageObjectUrl ?? null
  };
}

export function canExportPoster(
  form: PosterFormState,
  generated?: PosterData | null,
  aiCopy?: PosterAiCopyData | null
): boolean {
  return Boolean(resolveTitle(form, generated, aiCopy).trim());
}

export function posterExportFilename(model: PosterRenderModel): string {
  const slug = model.title
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9\u0980-\u09FF]+/gi, "_")
    .replace(/^_|_$/g, "")
    .slice(0, 48);
  const ratio = model.aspectRatio === "A4" ? "A4" : model.aspectRatio.replace(":", "x");
  return `poster_${slug || "design"}_${ratio}.png`;
}
