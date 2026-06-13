import { categoryLabel, PREVIEW_PALETTES } from "@/lib/news-photocard/constants";
import type {
  NewsPhotocardAiCopyData,
  NewsPhotocardData,
  NewsPhotocardFormState,
  NewsAspectRatioId,
  NewsDesignStyleId,
  NewsLanguageId,
  NewsToneId
} from "@/lib/news-photocard/types";

export type PhotocardPalette = (typeof PREVIEW_PALETTES)[NewsDesignStyleId];

export interface PhotocardRenderModel {
  headline: string;
  subheadline: string;
  category: string;
  dateStr: string;
  aspectRatio: NewsAspectRatioId;
  tone: NewsToneId;
  designStyle: NewsDesignStyleId;
  language: NewsLanguageId;
  palette: PhotocardPalette;
  logoObjectUrl: string | null;
  imageObjectUrl: string | null;
}

export const EXPORT_DIMENSIONS: Record<NewsAspectRatioId, { width: number; height: number }> = {
  "1:1": { width: 1080, height: 1080 },
  "4:5": { width: 1080, height: 1350 },
  "9:16": { width: 1080, height: 1920 }
};

export function formatPhotocardDate(language: NewsLanguageId): string {
  const now = new Date();
  if (language === "bn") {
    return now.toLocaleDateString("bn-BD", { day: "numeric", month: "short", year: "numeric" });
  }
  return now.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
}

export function resolveHeadline(
  form: NewsPhotocardFormState,
  generated?: NewsPhotocardData | null,
  aiCopy?: NewsPhotocardAiCopyData | null
): string {
  return generated?.headline ?? aiCopy?.headline ?? form.headline;
}

export function resolveSubheadline(
  form: NewsPhotocardFormState,
  generated?: NewsPhotocardData | null,
  aiCopy?: NewsPhotocardAiCopyData | null
): string {
  return generated?.subheadline ?? aiCopy?.subheadline ?? form.subheadline;
}

export function resolveCategory(
  form: NewsPhotocardFormState,
  generated?: NewsPhotocardData | null,
  aiCopy?: NewsPhotocardAiCopyData | null
): string {
  if (generated?.category) return generated.category;
  if (aiCopy) return categoryLabel(aiCopy.category);
  return categoryLabel(form.newsCategory);
}

export function buildPhotocardRenderModel(
  form: NewsPhotocardFormState,
  options?: {
    generated?: NewsPhotocardData | null;
    aiCopy?: NewsPhotocardAiCopyData | null;
    logoObjectUrl?: string | null;
    imageObjectUrl?: string | null;
  }
): PhotocardRenderModel {
  const tone = options?.aiCopy?.tone ?? form.tone;
  return {
    headline: resolveHeadline(form, options?.generated, options?.aiCopy),
    subheadline: resolveSubheadline(form, options?.generated, options?.aiCopy),
    category: resolveCategory(form, options?.generated, options?.aiCopy),
    dateStr: formatPhotocardDate(form.language),
    aspectRatio: form.aspectRatio,
    tone,
    designStyle: form.designStyle,
    language: form.language,
    palette: PREVIEW_PALETTES[form.designStyle],
    logoObjectUrl: options?.logoObjectUrl ?? null,
    imageObjectUrl: options?.imageObjectUrl ?? null
  };
}

export function canExportPhotocard(
  form: NewsPhotocardFormState,
  generated?: NewsPhotocardData | null,
  aiCopy?: NewsPhotocardAiCopyData | null
): boolean {
  return Boolean(resolveHeadline(form, generated, aiCopy).trim());
}

export function exportFilename(model: PhotocardRenderModel): string {
  const slug = model.headline
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9\u0980-\u09FF]+/gi, "_")
    .replace(/^_|_$/g, "")
    .slice(0, 48);
  return `news-photocard_${slug || "design"}_${model.aspectRatio.replace(":", "x")}.png`;
}
