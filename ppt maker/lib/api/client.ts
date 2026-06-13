import { mapIntentClassification, mapStudioProject } from "@/lib/content-studio/api-mapper";
import type {
  ContentGenerateRequest,
  ContentGenerateResponse,
  GenerationParameters,
  IntentClassification,
  PromptToDesignRequest,
  PromptToDesignResponse
} from "@/lib/content-studio/types";
import type {
  NewsPhotocardAiCopyRequest,
  NewsPhotocardAiCopyResponse,
  NewsPhotocardExportRequest,
  NewsPhotocardExportResponse,
  NewsPhotocardGenerateRequest,
  NewsPhotocardGenerateResponse
} from "@/lib/news-photocard/types";
import {
  AnalyzeResponse,
  AuthResponse,
  ExportPptxRequest,
  ExportPptxResponse,
  GenerateOutlineRequest,
  GenerateOutlineResponse,
  ListPresentationsResponse,
  PresentationRecord,
  ReviseOutlineRequest,
  ReviseOutlineResponse,
  SavePresentationRequest,
  SavePresentationResponse,
  UploadResponse
} from "@/lib/api/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

type RequestOptions = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  isFormData?: boolean;
  cache?: RequestCache;
};

function extractErrorMessage(data: unknown): string {
  if (typeof data !== "object" || data === null) {
    return "Request failed";
  }
  const record = data as Record<string, unknown>;
  if (typeof record.detail === "string") {
    return record.detail;
  }
  if (Array.isArray(record.detail) && record.detail.length > 0) {
    const first = record.detail[0];
    if (typeof first === "object" && first !== null && "msg" in first) {
      const msg = (first as { msg?: unknown }).msg;
      if (typeof msg === "string") {
        return msg;
      }
    }
    return JSON.stringify(record.detail);
  }
  if (typeof record.message === "string") {
    return record.message;
  }
  return "Request failed";
}

async function parseJson<T>(response: Response): Promise<T> {
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(extractErrorMessage(data));
  }

  return data as T;
}

async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, isFormData = false, cache } = options;
  const headers: HeadersInit = isFormData ? {} : { "Content-Type": "application/json" };

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : isFormData ? (body as FormData) : JSON.stringify(body),
    cache
  });

  return parseJson<T>(response);
}

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  return apiRequest<UploadResponse>("/api/v1/upload", { method: "POST", body: formData, isFormData: true });
}

export async function analyzeDocument(file: File): Promise<AnalyzeResponse> {
  const formData = new FormData();
  formData.append("file", file);
  return apiRequest<AnalyzeResponse>("/api/v1/documents/analyze", { method: "POST", body: formData, isFormData: true });
}

export async function generateOutline(payload: GenerateOutlineRequest): Promise<GenerateOutlineResponse> {
  return apiRequest<GenerateOutlineResponse>("/api/v1/outlines/generate", { method: "POST", body: payload });
}

export async function reviseOutline(payload: ReviseOutlineRequest): Promise<ReviseOutlineResponse> {
  return apiRequest<ReviseOutlineResponse>("/api/v1/outlines/revise", { method: "POST", body: payload });
}

export async function exportPptx(payload: ExportPptxRequest): Promise<ExportPptxResponse> {
  return apiRequest<ExportPptxResponse>("/api/v1/exports/pptx", { method: "POST", body: payload });
}

export async function downloadPptx(downloadUrl: string): Promise<Blob> {
  const response = await fetch(`${API_BASE_URL}${downloadUrl}`, { method: "GET" });
  if (!response.ok) {
    throw new Error("Failed to download PPTX file.");
  }
  return response.blob();
}

export async function savePresentation(payload: SavePresentationRequest): Promise<SavePresentationResponse> {
  return apiRequest<SavePresentationResponse>("/api/v1/presentations", { method: "POST", body: payload });
}

export async function listPresentations(userId?: string): Promise<ListPresentationsResponse> {
  const query = userId ? `?user_id=${encodeURIComponent(userId)}` : "";
  return apiRequest<ListPresentationsResponse>(`/api/v1/presentations${query}`, { cache: "no-store" });
}

export async function getPresentation(presentationId: string, userId?: string): Promise<PresentationRecord> {
  const query = userId ? `?user_id=${encodeURIComponent(userId)}` : "";
  return apiRequest<PresentationRecord>(`/api/v1/presentations/${presentationId}${query}`, { cache: "no-store" });
}

export async function regeneratePresentation(presentationId: string, userId?: string): Promise<SavePresentationResponse> {
  const query = userId ? `?user_id=${encodeURIComponent(userId)}` : "";
  return apiRequest<SavePresentationResponse>(`/api/v1/presentations/${presentationId}/regenerate${query}`, { method: "POST" });
}

export async function signUp(email: string, password: string, name?: string): Promise<AuthResponse> {
  return apiRequest<AuthResponse>("/api/v1/auth/signup", {
    method: "POST",
    body: { email, password, name }
  });
}

export async function signInBackend(email: string, password: string): Promise<AuthResponse> {
  return apiRequest<AuthResponse>("/api/v1/auth/signin", {
    method: "POST",
    body: { email, password }
  });
}

export async function generateContent(payload: ContentGenerateRequest): Promise<ContentGenerateResponse> {
  const raw = await apiRequest<{ success: boolean; message: string; project: Record<string, unknown> }>(
    "/api/v1/content/generate",
    { method: "POST", body: payload }
  );
  return {
    success: raw.success,
    message: raw.message,
    project: mapStudioProject(raw.project)
  };
}

export async function generateNewsPhotocard(
  payload: NewsPhotocardGenerateRequest
): Promise<NewsPhotocardGenerateResponse> {
  return apiRequest<NewsPhotocardGenerateResponse>("/api/v1/content/generate/news-photocard", {
    method: "POST",
    body: payload
  });
}

export async function generateNewsPhotocardAiCopy(
  payload: NewsPhotocardAiCopyRequest
): Promise<NewsPhotocardAiCopyResponse> {
  return apiRequest<NewsPhotocardAiCopyResponse>("/api/v1/content/generate/news-photocard/ai-copy", {
    method: "POST",
    body: payload
  });
}

export async function registerNewsPhotocardExport(
  payload: NewsPhotocardExportRequest
): Promise<NewsPhotocardExportResponse> {
  return apiRequest<NewsPhotocardExportResponse>("/api/v1/content/export/news-photocard", {
    method: "POST",
    body: payload
  });
}

export async function classifyIntent(prompt: string): Promise<IntentClassification> {
  const raw = await apiRequest<Record<string, unknown>>("/api/v1/content/classify-intent", {
    method: "POST",
    body: { prompt }
  });
  return mapIntentClassification(raw);
}

function toApiParameters(params: GenerationParameters) {
  return {
    refined_prompt: params.refinedPrompt,
    title: params.title,
    quantity: params.quantity,
    aspect_ratio: params.aspectRatio,
    language: params.language
  };
}

export async function promptToDesign(payload: PromptToDesignRequest): Promise<PromptToDesignResponse> {
  const raw = await apiRequest<{
    success: boolean;
    message: string;
    classification: Record<string, unknown>;
    project: Record<string, unknown> | null;
  }>("/api/v1/content/prompt-to-design", {
    method: "POST",
    body: {
      prompt: payload.prompt,
      category_id: payload.category_id ?? null,
      parameters: payload.parameters ? toApiParameters(payload.parameters) : null,
      brand_kit: payload.brand_kit ?? null
    }
  });
  return {
    success: raw.success,
    message: raw.message,
    classification: mapIntentClassification(raw.classification),
    project: raw.project ? mapStudioProject(raw.project) : null
  };
}
