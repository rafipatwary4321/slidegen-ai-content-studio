export type AspectRatioId = "1:1" | "4:5" | "16:9" | "9:16" | "A4";

export type ExportFormatId = "png" | "jpg" | "pdf" | "pptx" | "zip";

export type WorkflowId = "prompt" | "template" | "upload";

export type LanguageCode = "en" | "es" | "fr" | "de" | "ar" | "hi" | "bn" | "pt";

export interface AspectRatioOption {
  id: AspectRatioId;
  label: string;
  width: number;
  height: number;
}

export interface BrandKit {
  name: string;
  primaryColor: string;
  secondaryColor: string;
  accentColor: string;
  fontHeading: string;
  fontBody: string;
  logoUrl?: string;
}

export interface StudioTemplate {
  id: string;
  categoryId: string;
  title: string;
  subtitle: string;
  aspectRatio: AspectRatioId;
  featured?: boolean;
  gradient: string;
}

export interface ContentCategory {
  id: string;
  name: string;
  description: string;
  icon: string;
  defaultAspectRatio: AspectRatioId;
  supportedAspectRatios: AspectRatioId[];
  supportedExports: ExportFormatId[];
  gradient: string;
  tags: string[];
  /** Presentations use legacy /dashboard/new flow */
  legacyRoute?: string;
}

export interface CanvasLayer {
  id: string;
  type: "text" | "image" | "shape" | "group";
  name: string;
  x: number;
  y: number;
  width: number;
  height: number;
  rotation: number;
  opacity: number;
  visible: boolean;
  locked: boolean;
  content?: string;
  fill?: string;
  zIndex: number;
}

export interface StudioProject {
  id: string;
  categoryId: string;
  title: string;
  aspectRatio: AspectRatioId;
  language: LanguageCode;
  workflow: WorkflowId;
  templateId?: string;
  prompt: string;
  layers: CanvasLayer[];
  createdAt: string;
  updatedAt: string;
}

export interface ContentGenerateRequest {
  category_id: string;
  prompt: string;
  aspect_ratio: AspectRatioId;
  language?: LanguageCode;
  workflow: WorkflowId;
  template_id?: string | null;
  brand_kit?: BrandKit | null;
  document_text?: string | null;
}

export interface ContentGenerateResponse {
  success: boolean;
  message: string;
  project: StudioProject;
}

export interface GenerationParameters {
  refinedPrompt: string;
  title?: string | null;
  quantity?: number | null;
  aspectRatio?: AspectRatioId | null;
  language: LanguageCode;
}

export interface IntentAlternative {
  categoryId: string;
  categoryName: string;
  confidence: number;
}

export interface IntentClassification {
  success: boolean;
  categoryId: string;
  categoryName: string;
  confidence: number;
  reasoning: string;
  requiresManualSelection: boolean;
  parameters: GenerationParameters;
  alternatives: IntentAlternative[];
}

export interface PromptToDesignRequest {
  prompt: string;
  category_id?: string | null;
  parameters?: GenerationParameters | null;
  brand_kit?: BrandKit | null;
}

export interface PromptToDesignResponse {
  success: boolean;
  message: string;
  classification: IntentClassification;
  project?: StudioProject | null;
}
