"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { registerNewsPhotocardExport } from "@/lib/api/client";
import {
  buildPhotocardRenderModel,
  canExportPhotocard,
  exportFilename
} from "@/lib/news-photocard/render-model";
import { downloadPngBlob, exportNewsPhotocardPng } from "@/lib/news-photocard/export-png";
import type {
  NewsPhotocardAiCopyData,
  NewsPhotocardData,
  NewsPhotocardFormState
} from "@/lib/news-photocard/types";

interface ExportPngButtonProps {
  form: NewsPhotocardFormState;
  generated?: NewsPhotocardData | null;
  aiCopy?: NewsPhotocardAiCopyData | null;
  logoObjectUrl?: string | null;
  imageObjectUrl?: string | null;
}

export function ExportPngButton({
  form,
  generated,
  aiCopy,
  logoObjectUrl = null,
  imageObjectUrl = null
}: ExportPngButtonProps) {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canExport = canExportPhotocard(form, generated, aiCopy);

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
      const model = buildPhotocardRenderModel(form, {
        generated,
        aiCopy,
        logoObjectUrl,
        imageObjectUrl
      });

      const blob = await exportNewsPhotocardPng(model);
      downloadPngBlob(blob, exportFilename(model));

      try {
        await registerNewsPhotocardExport({
          headline: model.headline,
          subheadline: model.subheadline,
          category: model.category,
          aspect_ratio: model.aspectRatio,
          tone: model.tone,
          design_style: model.designStyle,
          language: model.language,
          has_logo: Boolean(logoObjectUrl),
          has_image: Boolean(imageObjectUrl)
        });
      } catch {
        // Manifest registration is optional — PNG download already succeeded.
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
