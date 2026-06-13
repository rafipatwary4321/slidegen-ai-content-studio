"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { registerPosterExport } from "@/lib/api/client";
import { downloadPngBlob, exportPosterPng } from "@/lib/poster/export-png";
import { buildPosterRenderModel, canExportPoster, posterExportFilename } from "@/lib/poster/render-model";
import type { PosterAiCopyData, PosterData, PosterFormState } from "@/lib/poster/types";

interface PosterExportPngButtonProps {
  form: PosterFormState;
  generated?: PosterData | null;
  aiCopy?: PosterAiCopyData | null;
  logoObjectUrl?: string | null;
  imageObjectUrl?: string | null;
}

export function PosterExportPngButton({
  form,
  generated,
  aiCopy,
  logoObjectUrl = null,
  imageObjectUrl = null
}: PosterExportPngButtonProps) {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canExport = canExportPoster(form, generated, aiCopy);

  useEffect(() => {
    if (!success) return;
    const timer = window.setTimeout(() => setSuccess(false), 3000);
    return () => window.clearTimeout(timer);
  }, [success]);

  async function handleExport() {
    if (!canExport) return;

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const model = buildPosterRenderModel(form, {
        generated,
        aiCopy,
        logoObjectUrl,
        imageObjectUrl
      });

      const blob = await exportPosterPng(model);
      downloadPngBlob(blob, posterExportFilename(model));

      try {
        await registerPosterExport({
          title: model.title,
          subtitle: model.subtitle,
          poster_type: form.posterType,
          aspect_ratio: model.aspectRatio,
          design_tone: model.designTone,
          language: model.language,
          date_time: model.dateTime || null,
          venue: model.venue || null,
          organizer: model.organizer || null,
          cta_text: model.ctaText,
          has_logo: Boolean(logoObjectUrl),
          has_image: Boolean(imageObjectUrl)
        });
      } catch {
        // Manifest registration is optional.
      }

      setSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "PNG export failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-2">
      <Button size="sm" className="w-full" onClick={handleExport} disabled={loading || !canExport}>
        {success ? <CheckCircle2 className="h-3.5 w-3.5" /> : <Download className="h-3.5 w-3.5" />}
        {loading ? "Exporting PNG…" : success ? "PNG downloaded" : "Export PNG"}
      </Button>
      {error ? <p className="text-xs text-rose-300">{error}</p> : null}
      {success ? <p className="text-xs text-emerald-300">Saved at full resolution ({form.aspectRatio}).</p> : null}
    </div>
  );
}
