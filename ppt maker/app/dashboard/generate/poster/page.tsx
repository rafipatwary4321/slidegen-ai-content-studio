"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { PosterForm } from "@/components/poster/poster-form";
import { PosterPreview } from "@/components/poster/poster-preview";
import { GeneratorShell } from "@/components/ui/generator-shell";
import { generatePoster, generatePosterAiCopy } from "@/lib/api/client";
import { CATEGORY_TO_POSTER_TYPE } from "@/lib/poster/constants";
import {
  DEFAULT_POSTER_FORM,
  type PosterAiCopyData,
  type PosterData,
  type PosterFormState,
  type PosterTypeId
} from "@/lib/poster/types";

function PosterGeneratorFallback() {
  return (
    <div className="space-y-6 pb-12">
      <div className="h-8 w-36 animate-pulse rounded-full bg-white/10" />
      <div className="panel animate-pulse">
        <div className="h-8 w-64 rounded bg-white/10" />
        <div className="mt-4 h-24 rounded bg-white/5" />
      </div>
    </div>
  );
}

function PosterGeneratorContent() {
  const searchParams = useSearchParams();
  const [form, setForm] = useState<PosterFormState>(DEFAULT_POSTER_FORM);
  const [generated, setGenerated] = useState<PosterData | null>(null);
  const [aiCopy, setAiCopy] = useState<PosterAiCopyData | null>(null);
  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const typeParam = searchParams.get("type");
    if (typeParam && typeParam in CATEGORY_TO_POSTER_TYPE) {
      setForm((prev) => ({ ...prev, posterType: CATEGORY_TO_POSTER_TYPE[typeParam] as PosterTypeId }));
    } else if (typeParam && ["event", "political", "educational", "business", "awareness", "product"].includes(typeParam)) {
      setForm((prev) => ({ ...prev, posterType: typeParam as PosterTypeId }));
    }
  }, [searchParams]);

  function applyAiCopy(data: PosterAiCopyData) {
    setAiCopy(data);
    setForm((prev) => ({
      ...prev,
      title: data.title,
      subtitle: data.subtitle,
      ctaText: data.ctaText,
      posterType: data.posterType,
      designTone: data.designTone
    }));
  }

  async function handleAiCopy() {
    const prompt = form.aiPrompt.trim();
    if (!prompt) {
      setError("Enter a rough poster prompt for AI copy generation.");
      return;
    }

    setAiLoading(true);
    setError(null);

    try {
      const response = await generatePosterAiCopy({ prompt, language: form.language });
      applyAiCopy(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "AI copy generation failed.");
    } finally {
      setAiLoading(false);
    }
  }

  async function handleGenerate() {
    if (!form.title.trim() && !form.aiPrompt.trim()) {
      setError("Enter a poster title or an AI prompt.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      let workingForm = form;

      if (!form.title.trim() && form.aiPrompt.trim()) {
        const copyResponse = await generatePosterAiCopy({
          prompt: form.aiPrompt.trim(),
          language: form.language
        });
        applyAiCopy(copyResponse.data);
        workingForm = {
          ...form,
          title: copyResponse.data.title,
          subtitle: copyResponse.data.subtitle,
          ctaText: copyResponse.data.ctaText,
          posterType: copyResponse.data.posterType,
          designTone: copyResponse.data.designTone
        };
      }

      const response = await generatePoster({
        title: workingForm.title.trim(),
        subtitle: workingForm.subtitle.trim(),
        poster_type: workingForm.posterType,
        date_time: workingForm.dateTime.trim() || null,
        venue: workingForm.venue.trim() || null,
        organizer: workingForm.organizer.trim() || null,
        cta_text: workingForm.ctaText.trim() || "Learn More",
        language: workingForm.language,
        aspect_ratio: workingForm.aspectRatio,
        design_tone: workingForm.designTone,
        ai_prompt: workingForm.aiPrompt.trim() || null,
        has_logo: Boolean(workingForm.logoFile),
        has_image: Boolean(workingForm.imageFile)
      });
      setGenerated(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Generation failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <GeneratorShell
      eyebrow="Content Studio"
      title="Poster Generator"
      description="Describe your poster in plain words — AI drafts polished title, subtitle, CTA, type, and tone."
      accent="violet"
      error={error}
    >
      <div className="studio-generator-grid">
        <PosterForm
          value={form}
          onChange={setForm}
          onGenerate={handleGenerate}
          onAiCopy={handleAiCopy}
          loading={loading}
          aiLoading={aiLoading}
        />
        <PosterPreview form={form} generated={generated} aiCopy={aiCopy} />
      </div>
    </GeneratorShell>
  );
}

export default function PosterGeneratorPage() {
  return (
    <Suspense fallback={<PosterGeneratorFallback />}>
      <PosterGeneratorContent />
    </Suspense>
  );
}
