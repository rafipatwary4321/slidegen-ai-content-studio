export type PosterTypeId = "event" | "political" | "educational" | "business" | "awareness" | "product";

export type PosterLanguageId = "en" | "bn";

export type PosterAspectRatioId = "1:1" | "4:5" | "9:16" | "A4";

export type PosterDesignToneId =
  | "premium-corporate"
  | "bold-political"
  | "modern-youth"
  | "academic-clean"
  | "luxury-event";

export interface PosterFormState {
  title: string;
  subtitle: string;
  posterType: PosterTypeId;
  dateTime: string;
  venue: string;
  organizer: string;
  ctaText: string;
  language: PosterLanguageId;
  aspectRatio: PosterAspectRatioId;
  designTone: PosterDesignToneId;
  aiPrompt: string;
  logoFile: File | null;
  imageFile: File | null;
}

export interface PosterGenerateRequest {
  title: string;
  subtitle: string;
  poster_type: PosterTypeId;
  date_time?: string | null;
  venue?: string | null;
  organizer?: string | null;
  cta_text: string;
  language: PosterLanguageId;
  aspect_ratio: PosterAspectRatioId;
  design_tone: PosterDesignToneId;
  ai_prompt?: string | null;
  has_logo: boolean;
  has_image: boolean;
}

export interface PosterData {
  title: string;
  subtitle: string;
  posterType: PosterTypeId;
  language: PosterLanguageId;
  aspectRatio: PosterAspectRatioId;
  designTone: PosterDesignToneId;
  layoutInstructions: string;
  exportReadyData: Record<string, unknown>;
}

export interface PosterGenerateResponse {
  success: boolean;
  message: string;
  data: PosterData;
}

export interface PosterAiCopyRequest {
  prompt: string;
  language: PosterLanguageId;
}

export interface PosterAiCopyData {
  title: string;
  subtitle: string;
  ctaText: string;
  posterType: PosterTypeId;
  designTone: PosterDesignToneId;
  layoutDirection: string;
  source: "openai" | "mock";
}

export interface PosterAiCopyResponse {
  success: boolean;
  message: string;
  data: PosterAiCopyData;
}

export interface PosterExportRequest {
  title: string;
  subtitle: string;
  poster_type: PosterTypeId;
  aspect_ratio: PosterAspectRatioId;
  design_tone: PosterDesignToneId;
  language: PosterLanguageId;
  date_time?: string | null;
  venue?: string | null;
  organizer?: string | null;
  cta_text: string;
  has_logo: boolean;
  has_image: boolean;
}

export interface PosterExportResponse {
  success: boolean;
  message: string;
  export_id: string;
  manifest_url: string;
  server_png_ready: boolean;
}

export const DEFAULT_POSTER_FORM: PosterFormState = {
  title: "Annual Innovation Summit 2026",
  subtitle: "Ideas, leaders, and breakthroughs shaping the future of technology.",
  posterType: "event",
  dateTime: "Saturday, 14 June 2026 · 10:00 AM",
  venue: "Grand Convention Hall, Dhaka",
  organizer: "SlideGen Events",
  ctaText: "Register Now",
  language: "en",
  aspectRatio: "A4",
  designTone: "luxury-event",
  aiPrompt: "",
  logoFile: null,
  imageFile: null
};
