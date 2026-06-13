"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowLeft } from "lucide-react";
import { NewsPhotocardForm } from "@/components/news-photocard/news-photocard-form";
import { NewsPhotocardPreview } from "@/components/news-photocard/news-photocard-preview";
import { PageHeader } from "@/components/ui/page-header";
import { ErrorBanner } from "@/components/ui/inline-feedback";
import { generateNewsPhotocard, generateNewsPhotocardAiCopy } from "@/lib/api/client";
import {
  DEFAULT_NEWS_PHOTOCARD_FORM,
  type NewsPhotocardAiCopyData,
  type NewsPhotocardData,
  type NewsPhotocardFormState
} from "@/lib/news-photocard/types";

export default function NewsPhotocardGeneratorPage() {
  const [form, setForm] = useState<NewsPhotocardFormState>(DEFAULT_NEWS_PHOTOCARD_FORM);
  const [generated, setGenerated] = useState<NewsPhotocardData | null>(null);
  const [aiCopy, setAiCopy] = useState<NewsPhotocardAiCopyData | null>(null);
  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function applyAiCopy(data: NewsPhotocardAiCopyData) {
    setAiCopy(data);
    setForm((prev) => ({
      ...prev,
      headline: data.headline,
      subheadline: data.subheadline,
      newsCategory: data.category,
      tone: data.tone
    }));
  }

  async function handleAiCopy() {
    const prompt = form.aiPrompt.trim();
    if (!prompt) {
      setError("Enter a rough story prompt for AI copy generation.");
      return;
    }

    setAiLoading(true);
    setError(null);

    try {
      const response = await generateNewsPhotocardAiCopy({
        prompt,
        language: form.language
      });
      applyAiCopy(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "AI copy generation failed.");
    } finally {
      setAiLoading(false);
    }
  }

  async function handleGenerate() {
    if (!form.headline.trim() && !form.aiPrompt.trim()) {
      setError("Enter a headline or an AI prompt.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      let workingForm = form;

      if (!form.headline.trim() && form.aiPrompt.trim()) {
        const copyResponse = await generateNewsPhotocardAiCopy({
          prompt: form.aiPrompt.trim(),
          language: form.language
        });
        applyAiCopy(copyResponse.data);
        workingForm = {
          ...form,
          headline: copyResponse.data.headline,
          subheadline: copyResponse.data.subheadline,
          newsCategory: copyResponse.data.category,
          tone: copyResponse.data.tone
        };
      }

      const response = await generateNewsPhotocard({
        headline: workingForm.headline.trim(),
        subheadline: workingForm.subheadline.trim(),
        news_category: workingForm.newsCategory,
        language: workingForm.language,
        aspect_ratio: workingForm.aspectRatio,
        tone: workingForm.tone,
        design_style: workingForm.designStyle,
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
    <div className="space-y-6 pb-10">
      <Link href="/dashboard" className="inline-flex items-center gap-1 text-xs text-slate-400 hover:text-white">
        <ArrowLeft className="h-3.5 w-3.5" /> Marketplace
      </Link>

      <PageHeader
        eyebrow="Content Studio"
        title="News Photocard Generator"
        description="Describe a story in plain words — AI drafts professional headline and subheadline for your photocard."
      />

      {error ? <ErrorBanner message={error} /> : null}

      <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_minmax(320px,420px)]">
        <NewsPhotocardForm
          value={form}
          onChange={setForm}
          onGenerate={handleGenerate}
          onAiCopy={handleAiCopy}
          loading={loading}
          aiLoading={aiLoading}
        />
        <NewsPhotocardPreview form={form} generated={generated} aiCopy={aiCopy} />
      </div>
    </div>
  );
}
