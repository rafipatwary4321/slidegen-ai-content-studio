import type { AspectRatioOption, ExportFormatId, LanguageCode } from "@/lib/content-studio/types";

export const ASPECT_RATIOS: AspectRatioOption[] = [
  { id: "1:1", label: "Square 1:1", width: 1080, height: 1080 },
  { id: "4:5", label: "Portrait 4:5", width: 1080, height: 1350 },
  { id: "16:9", label: "Widescreen 16:9", width: 1920, height: 1080 },
  { id: "9:16", label: "Story 9:16", width: 1080, height: 1920 },
  { id: "A4", label: "Print A4", width: 2480, height: 3508 }
];

export const EXPORT_FORMATS: { id: ExportFormatId; label: string }[] = [
  { id: "png", label: "PNG" },
  { id: "jpg", label: "JPG" },
  { id: "pdf", label: "PDF" },
  { id: "pptx", label: "PPTX" },
  { id: "zip", label: "ZIP Bundle" }
];

export const LANGUAGES: { code: LanguageCode; label: string }[] = [
  { code: "en", label: "English" },
  { code: "es", label: "Español" },
  { code: "fr", label: "Français" },
  { code: "de", label: "Deutsch" },
  { code: "ar", label: "العربية" },
  { code: "hi", label: "हिन्दी" },
  { code: "bn", label: "বাংলা" },
  { code: "pt", label: "Português" }
];

export const DEFAULT_BRAND_KIT = {
  name: "My Brand",
  primaryColor: "#8B5CF6",
  secondaryColor: "#22D3EE",
  accentColor: "#F472B6",
  fontHeading: "Inter",
  fontBody: "Inter"
};
