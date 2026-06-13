export type NewsCategoryId =
  | "politics"
  | "campus"
  | "sports"
  | "international"
  | "business"
  | "entertainment";

export type NewsLanguageId = "en" | "bn";

export type NewsAspectRatioId = "1:1" | "4:5" | "9:16";

export type NewsToneId = "breaking-news" | "premium-editorial" | "youth-media" | "corporate-press";

export type NewsDesignStyleId = "dark-red" | "black" | "white" | "gold";

export interface NewsPhotocardFormState {
  headline: string;
  subheadline: string;
  newsCategory: NewsCategoryId;
  language: NewsLanguageId;
  aspectRatio: NewsAspectRatioId;
  tone: NewsToneId;
  designStyle: NewsDesignStyleId;
  aiPrompt: string;
  logoFile: File | null;
  imageFile: File | null;
}

export interface NewsPhotocardGenerateRequest {
  headline: string;
  subheadline: string;
  news_category: NewsCategoryId;
  language: NewsLanguageId;
  aspect_ratio: NewsAspectRatioId;
  tone: NewsToneId;
  design_style: NewsDesignStyleId;
  ai_prompt?: string | null;
  has_logo: boolean;
  has_image: boolean;
}

export interface NewsPhotocardData {
  title: string;
  headline: string;
  subheadline: string;
  category: string;
  language: NewsLanguageId;
  aspectRatio: NewsAspectRatioId;
  tone: NewsToneId;
  designStyle: NewsDesignStyleId;
  layoutInstructions: string;
  exportReadyData: Record<string, unknown>;
}

export interface NewsPhotocardGenerateResponse {
  success: boolean;
  message: string;
  data: NewsPhotocardData;
}

export interface NewsPhotocardAiCopyRequest {
  prompt: string;
  language: NewsLanguageId;
}

export interface NewsPhotocardAiCopyData {
  headline: string;
  subheadline: string;
  category: NewsCategoryId;
  tone: NewsToneId;
  layoutDirection: string;
  source: "openai" | "mock";
}

export interface NewsPhotocardAiCopyResponse {
  success: boolean;
  message: string;
  data: NewsPhotocardAiCopyData;
}

export interface NewsPhotocardExportRequest {
  headline: string;
  subheadline: string;
  category: string;
  aspect_ratio: NewsAspectRatioId;
  tone: NewsToneId;
  design_style: NewsDesignStyleId;
  language: NewsLanguageId;
  has_logo: boolean;
  has_image: boolean;
}

export interface NewsPhotocardExportResponse {
  success: boolean;
  message: string;
  export_id: string;
  manifest_url: string;
  server_png_ready: boolean;
}

export const DEFAULT_NEWS_PHOTOCARD_FORM: NewsPhotocardFormState = {
  headline: "Government Announces Major Policy Reform",
  subheadline: "Leaders outline sweeping changes expected to reshape the national agenda.",
  newsCategory: "politics",
  language: "en",
  aspectRatio: "4:5",
  tone: "breaking-news",
  designStyle: "dark-red",
  aiPrompt: "",
  logoFile: null,
  imageFile: null
};
