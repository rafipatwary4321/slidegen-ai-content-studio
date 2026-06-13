"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import { Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ExportPptxButton } from "@/components/presentation/export-pptx-button";
import { RevisionPanel } from "@/components/presentation/revision-panel";
import { ErrorBanner } from "@/components/ui/inline-feedback";
import { PageHeader } from "@/components/ui/page-header";
import { getPresentation, reviseOutline } from "@/lib/api/client";
import { Persona, PresentationRecord, SlideOutlineItem, Theme } from "@/lib/api/types";

export default function PresentationDetailPage({ params }: { params: { id: string } }) {
  const { data: session, status } = useSession();
  const [record, setRecord] = useState<PresentationRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [theme, setTheme] = useState<Theme>("Cinematic Dark");
  const [persona, setPersona] = useState<Persona>("Business");
  const [revisionPrompt, setRevisionPrompt] = useState("Add one slide about risks");
  const [error, setError] = useState<string | null>(null);
  const [loadingRevision, setLoadingRevision] = useState(false);
  const [previousOutline, setPreviousOutline] = useState<SlideOutlineItem[] | null>(null);
  const [currentOutline, setCurrentOutline] = useState<SlideOutlineItem[]>([]);

  useEffect(() => {
    const userId = session?.user?.id;
    if (status === "loading") return;
    if (!userId) {
      setLoading(false);
      setRecord(null);
      setError("Please sign in to view this presentation.");
      return;
    }

    async function load() {
      setLoading(true);
      setError(null);
      try {
        const res = await getPresentation(params.id, userId);
        setRecord(res);
        setCurrentOutline(res.outline);
        setTheme(res.theme as Theme);
        setPersona(res.persona as Persona);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load presentation.");
      } finally {
        setLoading(false);
      }
    }
    void load();
  }, [params.id, session?.user?.id, status]);

  async function handleRevision() {
    setLoadingRevision(true);
    setError(null);
    try {
      const revised = await reviseOutline({
        instruction: revisionPrompt,
        persona,
        theme,
        outline: currentOutline,
        presentation_id: record?.id,
        user_id: session?.user?.id
      });
      setPreviousOutline(revised.previous_outline);
      setCurrentOutline(revised.updated_outline);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to revise presentation.");
    } finally {
      setLoadingRevision(false);
    }
  }

  if (loading) {
    return <div className="panel h-32 animate-pulse" />;
  }

  if (status === "loading") {
    return <div className="panel h-32 animate-pulse" />;
  }

  if (!record) {
    return (
      <div className="space-y-4">
        <p className="text-sm text-slate-300">Presentation not found.</p>
        <Link href="/dashboard/history" className="inline-flex text-sm text-cyan-300 transition hover:text-cyan-200">{"<-"} Back to history</Link>
      </div>
    );
  }

  return (
    <div className="space-y-6 sm:space-y-7">
      <PageHeader
        eyebrow="Presentation Detail"
        title={record.title}
        description="Inspect metadata, revise structure, and export the final deck."
        actions={
          <>
            <Button variant="secondary" size="sm"><Copy className="h-3.5 w-3.5" /> Duplicate</Button>
            <ExportPptxButton
              payload={{
                title: record.title,
                theme,
                slides: currentOutline,
                speaker_notes: record.speaker_notes,
                presentation_id: record.id,
                user_id: session?.user?.id
              }}
            />
          </>
        }
      />

      {error ? <ErrorBanner message={error} /> : null}

      <div className="grid gap-6 xl:grid-cols-2">
        <section className="panel">
          <h3 className="panel-title">Deck Metadata</h3>
          <ul className="mt-4 space-y-2 text-sm text-slate-300">
            <li>Uploaded file: {record.uploaded_filename}</li>
            <li>Slides: {currentOutline.length}</li>
            <li>Created: {new Date(record.created_at).toLocaleString()}</li>
            <li>Theme: {theme}</li>
            <li>Persona: {persona}</li>
            <li>PPT path: {record.pptx_file_path ?? "Not exported yet"}</li>
          </ul>
        </section>

        <section className="panel">
          <RevisionPanel
            instruction={revisionPrompt}
            onInstructionChange={setRevisionPrompt}
            onApply={handleRevision}
            loading={loadingRevision}
            disabled={!currentOutline.length}
          />
        </section>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <section className="panel">
          <h3 className="panel-title">Current Outline</h3>
          <ol className="mt-4 space-y-2 text-sm text-slate-300">
            {currentOutline.map((outline, idx) => (
              <li key={`${outline.title}-${idx}`} className="rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2.5">
                <span className="mr-2 text-cyan-200">{idx + 1}.</span>{outline.title}
              </li>
            ))}
          </ol>
        </section>

        <section className="panel">
          <h3 className="panel-title">Previous Outline</h3>
          <ol className="mt-4 space-y-2 text-sm text-slate-300">
            {(previousOutline ?? currentOutline).map((outline, idx) => (
              <li key={`prev-${outline.title}-${idx}`} className="rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2.5">
                <span className="mr-2 text-slate-400">{idx + 1}.</span>{outline.title}
              </li>
            ))}
          </ol>
        </section>
      </div>

      <Link href="/dashboard/history" className="inline-flex text-sm text-cyan-300 transition hover:text-cyan-200">{"<-"} Back to history</Link>
    </div>
  );
}
