"use client";

import type { IntentClassification } from "@/lib/content-studio/types";
import { getCategoryById } from "@/lib/content-studio/categories";
import { categoryIcon } from "@/lib/content-studio/icons";
import { Button } from "@/components/ui/button";
import { AlertCircle, ArrowRightLeft, Check, Sparkles } from "lucide-react";

interface IntentDetectionCardProps {
  classification: IntentClassification;
  onConfirm: () => void;
  onChangeCategory: () => void;
  loading?: boolean;
}

export function IntentDetectionCard({ classification, onConfirm, onChangeCategory, loading }: IntentDetectionCardProps) {
  const category = getCategoryById(classification.categoryId);
  const Icon = category ? categoryIcon(category.icon) : Sparkles;
  const pct = Math.round(classification.confidence * 100);
  const low = classification.requiresManualSelection;

  return (
    <div className={`rounded-2xl border p-4 ${low ? "border-amber-400/30 bg-amber-400/5" : "border-cyan-400/25 bg-cyan-400/5"}`}>
      <div className="flex flex-wrap items-start gap-4">
        <div className={`flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br ${category?.gradient ?? "from-violet-600 to-cyan-500"}`}>
          <Icon className="h-7 w-7 text-white" />
        </div>
        <div className="min-w-0 flex-1">
          <p className="text-[11px] font-medium uppercase tracking-wider text-slate-400">Detected category</p>
          <h3 className="mt-1 text-lg font-semibold text-white">{classification.categoryName}</h3>
          <p className="mt-1 text-sm text-slate-300">{classification.reasoning}</p>
          <div className="mt-2 flex flex-wrap gap-2 text-xs text-slate-400">
            <span className="rounded-full bg-white/10 px-2.5 py-1">{pct}% confidence</span>
            {classification.parameters.quantity ? (
              <span className="rounded-full bg-white/10 px-2.5 py-1">Qty: {classification.parameters.quantity}</span>
            ) : null}
            {classification.parameters.aspectRatio ? (
              <span className="rounded-full bg-white/10 px-2.5 py-1">{classification.parameters.aspectRatio}</span>
            ) : null}
          </div>
          {low ? (
            <p className="mt-2 inline-flex items-center gap-1.5 text-xs text-amber-200">
              <AlertCircle className="h-3.5 w-3.5" /> Low confidence — confirm or pick another category.
            </p>
          ) : null}
        </div>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        <Button size="sm" onClick={onConfirm} disabled={loading}>
          <Check className="h-3.5 w-3.5" /> {loading ? "Generating…" : "Confirm & generate"}
        </Button>
        <Button size="sm" variant="secondary" onClick={onChangeCategory} disabled={loading}>
          <ArrowRightLeft className="h-3.5 w-3.5" /> Change category
        </Button>
      </div>
    </div>
  );
}
