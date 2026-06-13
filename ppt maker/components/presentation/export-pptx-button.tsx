"use client";

import { useState } from "react";
import { Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { downloadPptx, exportPptx } from "@/lib/api/client";
import { ExportPptxRequest } from "@/lib/api/types";

interface ExportPptxButtonProps {
  payload: ExportPptxRequest;
}

export function ExportPptxButton({ payload }: ExportPptxButtonProps) {
  const [loading, setLoading] = useState(false);

  async function handleExport() {
    setLoading(true);
    try {
      const exportResponse = await exportPptx(payload);
      const blob = await downloadPptx(exportResponse.export.download_url);
      const objectUrl = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = objectUrl;
      anchor.download = `${payload.title.replace(/\s+/g, "_")}.pptx`;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      URL.revokeObjectURL(objectUrl);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Failed to export PPTX.";
      window.alert(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Button size="sm" onClick={handleExport} disabled={loading}>
      <Download className="h-3.5 w-3.5" />
      {loading ? "Exporting..." : "Export PPTX"}
    </Button>
  );
}
