"use client";

import { useMemo, useState } from "react";
import { BarChart3, CheckCircle2, UserRound } from "lucide-react";
import { useSession } from "next-auth/react";
import { UploadBox } from "@/components/forms/upload-box";
import { PersonaSelector } from "@/components/forms/persona-selector";
import { ThemeSelector } from "@/components/forms/theme-selector";
import { PromptInput } from "@/components/forms/prompt-input";
import { ExportPptxButton } from "@/components/presentation/export-pptx-button";
import { OutlinePreview } from "@/components/presentation/outline-preview";
import { RevisionPanel } from "@/components/presentation/revision-panel";
import { PageHeader } from "@/components/ui/page-header";
import { EmptyState } from "@/components/ui/empty-state";
import { ErrorBanner, LoadingCardGrid } from "@/components/ui/inline-feedback";
import { analyzeDocument, generateOutline, reviseOutline, savePresentation, uploadDocument } from "@/lib/api/client";
import { AnalyzeResponse, Persona, SlideOutlineItem, SpeakerNoteItem, Theme } from "@/lib/api/types";

export default function NewPresentationPage() {
  const { data: session, status } = useSession();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [persona, setPersona] = useState<Persona>("Business");
  const [theme, setTheme] = useState<Theme>("Cinematic Dark");
  const [prompt, setPrompt] = useState("Make it more professional");
  const [loadingGenerate, setLoadingGenerate] = useState(false);
  const [loadingRevision, setLoadingRevision] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [currentOutline, setCurrentOutline] = useState<SlideOutlineItem[]>([]);
  const [previousOutline, setPreviousOutline] = useState<SlideOutlineItem[] | null>(null);
  const [speakerNotes, setSpeakerNotes] = useState<SpeakerNoteItem[]>([]);
  const [revisionPrompt, setRevisionPrompt] = useState("Make it more professional");
  const [savedPresentationId, setSavedPresentationId] = useState<string | null>(null);

  function handleFileSelect(file: File | null) {
    setSelectedFile(file);
    setResult(null);
    setError(null);
    setCurrentOutline([]);
    setPreviousOutline(null);
    setSpeakerNotes([]);
    setSavedPresentationId(null);
  }

  const outlineTitles = useMemo(() => {
    if (currentOutline.length) return currentOutline.map((slide) => slide.title);
    return ["Upload and generate to preview your AI outline."];
  }, [currentOutline]);

  async function handleGenerate() {
    if (!selectedFile) {
      setError("Please select a PDF, DOCX, or TXT file first.");
      return;
    }

    setLoadingGenerate(true);
    setError(null);

    try {
      await uploadDocument(selectedFile);
      const analyze = await analyzeDocument(selectedFile);

      let outlinePersona = persona;
      const detected = analyze.analysis.persona;
      if (detected === "Student" || detected === "Business" || detected === "Marketing" || detected === "Corporate") {
        outlinePersona = detected;
        setPersona(detected);
      }

      let outlineTheme = theme;
      const rec = analyze.analysis.recommended_theme;
      if (rec === "Cinematic Dark" || rec === "Professional Light") {
        outlineTheme = rec;
        setTheme(rec);
      }

      const outlineResponse = await generateOutline({
        document_summary: analyze.analysis.summary,
        persona: outlinePersona,
        theme: outlineTheme,
        prompt,
        max_slides: 8
      });
      setResult(analyze);
      setCurrentOutline(outlineResponse.outline);
      setPreviousOutline(null);
      setSpeakerNotes(analyze.analysis.speaker_notes);

      if (session?.user?.id) {
        const saved = await savePresentation({
          title: analyze.analysis.presentation_title,
          uploaded_filename: analyze.parsed_document.metadata.filename,
          persona: outlinePersona,
          theme: outlineTheme,
          outline: outlineResponse.outline,
          speaker_notes: analyze.analysis.speaker_notes,
          user_id: session.user.id
        });
        setSavedPresentationId(saved.presentation.id);
      } else {
        setSavedPresentationId(null);
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to generate presentation.";
      setError(message);
    } finally {
      setLoadingGenerate(false);
    }
  }

  async function handleRevision() {
    if (!currentOutline.length) {
      setError("Generate an initial outline before applying revision.");
      return;
    }
    setLoadingRevision(true);
    setError(null);
    try {
      const revised = await reviseOutline({
        instruction: revisionPrompt,
        persona,
        theme,
        outline: currentOutline,
        presentation_id: savedPresentationId ?? undefined,
        user_id: session?.user?.id
      });
      setPreviousOutline(revised.previous_outline);
      setCurrentOutline(revised.updated_outline);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to revise outline.";
      setError(message);
    } finally {
      setLoadingRevision(false);
    }
  }

  return (
    <div className="space-y-6 sm:space-y-7">
      {status === "loading" ? <LoadingCardGrid /> : null}
      {!session?.user?.id && status !== "loading" ? (
        <p className="rounded-xl border border-white/10 bg-white/[0.03] px-4 py-3 text-xs text-slate-400">
          Sign in to save presentations to history. You can still generate and export without an account.
        </p>
      ) : null}
      <PageHeader
        eyebrow="Generator"
        title="New Presentation"
        description="Upload source material, select persona and theme, then generate a presentation draft."
      />

      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <div className="space-y-5">
          <UploadBox
            selectedFile={selectedFile}
            onFileSelect={handleFileSelect}
            disabled={loadingGenerate || loadingRevision}
          />
          <OutlinePreview items={outlineTitles} />
        </div>
        <div className="space-y-5">
          <PersonaSelector value={persona} onChange={setPersona} disabled={loadingGenerate || loadingRevision} />
          <ThemeSelector value={theme} onChange={setTheme} disabled={loadingGenerate || loadingRevision} />
          <PromptInput
            value={prompt}
            onChange={setPrompt}
            onGenerate={handleGenerate}
            loading={loadingGenerate}
            disabled={!selectedFile || loadingRevision}
          />
          <RevisionPanel
            instruction={revisionPrompt}
            onInstructionChange={setRevisionPrompt}
            onApply={handleRevision}
            loading={loadingRevision}
            disabled={!currentOutline.length || loadingGenerate}
          />
        </div>
      </div>

      {error ? <ErrorBanner message={error} /> : null}

      {!result && !loadingGenerate && !loadingRevision ? (
        <EmptyState
          title="No generated presentation yet"
          description="Select a file and click Generate Presentation to fetch title, persona, outline, chart suggestions, and speaker notes."
        />
      ) : null}

      {loadingGenerate || loadingRevision ? <LoadingCardGrid /> : null}

      {result ? (
        <div className="grid gap-5 lg:grid-cols-2">
          <section className="panel">
            <h3 className="panel-title">Presentation Summary</h3>
            <div className="mt-3 space-y-2 text-sm text-slate-300">
              <p className="text-base font-semibold text-white">{result.analysis.presentation_title}</p>
              <p className="inline-flex items-center gap-1"><UserRound className="h-3.5 w-3.5" /> Persona: {result.analysis.persona}</p>
              <p>Document type: {result.analysis.document_type}</p>
              <p>{result.analysis.summary}</p>
            </div>
          </section>

          <section className="panel">
            <h3 className="panel-title">Export Updated PPT</h3>
            <p className="panel-subtitle">Export the current revised outline and notes to PowerPoint.</p>
            <div className="mt-4">
              <ExportPptxButton
                payload={{
                  title: result.analysis.presentation_title,
                  theme,
                  slides: currentOutline,
                  speaker_notes: speakerNotes,
                  presentation_id: savedPresentationId ?? undefined,
                  user_id: session?.user?.id
                }}
              />
            </div>
          </section>

          <section className="panel">
            <h3 className="panel-title">Chart Suggestions</h3>
            <ul className="mt-3 space-y-2 text-sm text-slate-300">
              {result.analysis.chart_suggestions.length ? (
                result.analysis.chart_suggestions.map((item, idx) => (
                  <li key={`${item}-${idx}`} className="inline-flex w-full items-start gap-2 rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2">
                    <BarChart3 className="mt-0.5 h-3.5 w-3.5 text-cyan-300" />
                    <span>{item}</span>
                  </li>
                ))
              ) : (
                <li className="text-slate-400">No chart suggestion detected.</li>
              )}
            </ul>
          </section>

          <section className="panel lg:col-span-2">
            <h3 className="panel-title">Slide Outline</h3>
            <div className="mt-3 grid gap-3 md:grid-cols-2">
              {currentOutline.map((slide) => (
                <article key={slide.slide_number} className="rounded-xl border border-white/10 bg-white/[0.03] p-3">
                  <p className="text-sm font-semibold text-white">{slide.slide_number}. {slide.title}</p>
                  <ul className="mt-2 space-y-1 text-xs text-slate-300">
                    {slide.bullets.map((bullet, idx) => <li key={`${bullet}-${idx}`}>- {bullet}</li>)}
                  </ul>
                </article>
              ))}
            </div>
          </section>

          {previousOutline ? (
            <section className="panel lg:col-span-2">
              <h3 className="panel-title">Revision Diff Preview</h3>
              <div className="mt-3 grid gap-3 md:grid-cols-2">
                <div className="rounded-xl border border-white/10 bg-white/[0.03] p-3">
                  <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-400">Previous</p>
                  <ol className="mt-2 space-y-1 text-sm text-slate-300">
                    {previousOutline.map((slide) => (
                      <li key={`prev-${slide.slide_number}`}>{slide.slide_number}. {slide.title}</li>
                    ))}
                  </ol>
                </div>
                <div className="rounded-xl border border-cyan-300/30 bg-cyan-500/10 p-3">
                  <p className="text-xs font-semibold uppercase tracking-[0.16em] text-cyan-100">Updated</p>
                  <ol className="mt-2 space-y-1 text-sm text-slate-100">
                    {currentOutline.map((slide) => (
                      <li key={`new-${slide.slide_number}`}>{slide.slide_number}. {slide.title}</li>
                    ))}
                  </ol>
                </div>
              </div>
            </section>
          ) : null}

          <section className="panel lg:col-span-2">
            <h3 className="panel-title">Speaker Notes Preview</h3>
            <div className="mt-3 space-y-2">
              {speakerNotes.map((note) => (
                <div key={note.slide_number} className="rounded-xl border border-white/10 bg-white/[0.03] p-3 text-sm text-slate-300">
                  <p className="mb-1 inline-flex items-center gap-1 text-xs font-semibold text-cyan-200">
                    <CheckCircle2 className="h-3.5 w-3.5" /> Slide {note.slide_number}
                  </p>
                  <p>{note.note}</p>
                </div>
              ))}
            </div>
          </section>
        </div>
      ) : null}
    </div>
  );
}
