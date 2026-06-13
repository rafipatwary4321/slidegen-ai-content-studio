import type {
  AspectRatioId,
  CanvasLayer,
  GenerationParameters,
  IntentAlternative,
  IntentClassification,
  LanguageCode,
  StudioProject,
  WorkflowId
} from "@/lib/content-studio/types";

function mapLayer(raw: Record<string, unknown>): CanvasLayer {
  return {
    id: String(raw.id),
    type: (raw.type as CanvasLayer["type"]) ?? "text",
    name: String(raw.name ?? "Layer"),
    x: Number(raw.x ?? 0),
    y: Number(raw.y ?? 0),
    width: Number(raw.width ?? 100),
    height: Number(raw.height ?? 40),
    rotation: Number(raw.rotation ?? 0),
    opacity: Number(raw.opacity ?? 1),
    visible: raw.visible !== false,
    locked: Boolean(raw.locked),
    content: raw.content != null ? String(raw.content) : undefined,
    fill: raw.fill != null ? String(raw.fill) : undefined,
    zIndex: Number(raw.zIndex ?? 0)
  };
}

export function mapStudioProject(raw: Record<string, unknown>): StudioProject {
  const layers = Array.isArray(raw.layers) ? raw.layers.map((l) => mapLayer(l as Record<string, unknown>)) : [];
  return {
    id: String(raw.id),
    categoryId: String(raw.category_id),
    title: String(raw.title),
    aspectRatio: (raw.aspect_ratio as AspectRatioId) ?? "16:9",
    language: (raw.language as LanguageCode) ?? "en",
    workflow: (raw.workflow as WorkflowId) ?? "prompt",
    templateId: raw.template_id != null ? String(raw.template_id) : undefined,
    prompt: String(raw.prompt ?? ""),
    layers,
    createdAt: String(raw.created_at),
    updatedAt: String(raw.updated_at)
  };
}

function mapParameters(raw: Record<string, unknown>): GenerationParameters {
  return {
    refinedPrompt: String(raw.refined_prompt ?? ""),
    title: raw.title != null ? String(raw.title) : null,
    quantity: raw.quantity != null ? Number(raw.quantity) : null,
    aspectRatio: raw.aspect_ratio != null ? (raw.aspect_ratio as AspectRatioId) : null,
    language: (raw.language as LanguageCode) ?? "en"
  };
}

function mapAlternative(raw: Record<string, unknown>): IntentAlternative {
  return {
    categoryId: String(raw.category_id),
    categoryName: String(raw.category_name),
    confidence: Number(raw.confidence ?? 0)
  };
}

export function mapIntentClassification(raw: Record<string, unknown>): IntentClassification {
  const params = (raw.parameters as Record<string, unknown>) ?? {};
  const alts = Array.isArray(raw.alternatives)
    ? raw.alternatives.map((a) => mapAlternative(a as Record<string, unknown>))
    : [];
  return {
    success: Boolean(raw.success),
    categoryId: String(raw.category_id),
    categoryName: String(raw.category_name),
    confidence: Number(raw.confidence ?? 0),
    reasoning: String(raw.reasoning ?? ""),
    requiresManualSelection: Boolean(raw.requires_manual_selection),
    parameters: mapParameters(params),
    alternatives: alts
  };
}
