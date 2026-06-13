"use client";

import Link from "next/link";
import type { Route } from "next";
import { useCallback, useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import { Clock3, FileStack, History as HistoryIcon, RefreshCcw } from "lucide-react";
import { EmptyState } from "@/components/ui/empty-state";
import { ErrorBanner, LoadingCardGrid } from "@/components/ui/inline-feedback";
import { PageHeader } from "@/components/ui/page-header";
import { ExportPptxButton } from "@/components/presentation/export-pptx-button";
import { Button } from "@/components/ui/button";
import { listPresentations, regeneratePresentation } from "@/lib/api/client";
import { PresentationRecord, Theme } from "@/lib/api/types";

export default function HistoryPage() {
  const { data: session, status } = useSession();
  const [items, setItems] = useState<PresentationRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      if (!session?.user?.id) {
        setItems([]);
        return;
      }
      const res = await listPresentations(session.user.id);
      setItems(res.presentations);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load history.");
    } finally {
      setLoading(false);
    }
  }, [session?.user?.id]);

  useEffect(() => {
    if (status === "loading") return;
    void load();
  }, [session?.user?.id, status, load]);

  async function handleRegenerate(id: string) {
    setBusyId(id);
    try {
      await regeneratePresentation(id, session?.user?.id);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to regenerate.");
    } finally {
      setBusyId(null);
    }
  }

  return (
    <div className="space-y-6 sm:space-y-7">
      <PageHeader
        eyebrow="Library"
        title="History"
        description="Review previous generations, monitor status, and continue iterating your decks."
      />

      {error ? <ErrorBanner message={error} /> : null}

      {loading ? (
        <LoadingCardGrid />
      ) : status === "loading" ? (
        <LoadingCardGrid />
      ) : !items.length ? (
        <EmptyState
          title="No presentations yet"
          description="Generated decks will appear here with status, slides, and quick access to details."
          icon={<HistoryIcon className="h-5 w-5" />}
        />
      ) : (
        <div className="space-y-3">
          {items.map((item) => (
            <article
              key={item.id}
              className="panel group flex flex-col gap-4 p-4 transition hover:border-white/20 hover:bg-white/[0.07]"
            >
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm font-semibold text-white">{item.title}</p>
                  <div className="mt-1 flex flex-wrap items-center gap-3 text-xs text-slate-400">
                    <span className="inline-flex items-center gap-1"><FileStack className="h-3.5 w-3.5" /> {item.outline.length} slides</span>
                    <span className="inline-flex items-center gap-1"><Clock3 className="h-3.5 w-3.5" /> {new Date(item.created_at).toLocaleString()}</span>
                    <span>File: {item.uploaded_filename}</span>
                  </div>
                </div>
                <span className="w-fit rounded-full border border-cyan-300/30 bg-cyan-500/15 px-3 py-1 text-xs text-cyan-100">Saved</span>
              </div>

              <div className="flex flex-wrap gap-2">
                <Link href={`/dashboard/presentations/${item.id}` as Route}>
                  <Button size="sm" variant="secondary">View</Button>
                </Link>
                <Button size="sm" variant="secondary" onClick={() => handleRegenerate(item.id)} disabled={busyId === item.id}>
                  <RefreshCcw className="h-3.5 w-3.5" /> {busyId === item.id ? "Regenerating..." : "Regenerate"}
                </Button>
                <ExportPptxButton
                  payload={{
                    title: item.title,
                    theme: item.theme as Theme,
                    slides: item.outline,
                    speaker_notes: item.speaker_notes,
                    presentation_id: item.id,
                    user_id: session?.user?.id
                  }}
                />
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
