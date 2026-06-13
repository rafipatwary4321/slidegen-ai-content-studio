"use client";

import Link from "next/link";
import type { Route } from "next";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect } from "react";
import { ArrowLeft, Presentation } from "lucide-react";
import { Button } from "@/components/ui/button";
import { getCategoryById } from "@/lib/content-studio/categories";
import { categoryIcon } from "@/lib/content-studio/icons";

interface CategoryWorkspaceProps {
  categoryId: string;
}

export function CategoryWorkspace({ categoryId }: CategoryWorkspaceProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const category = getCategoryById(categoryId);
  const prompt = searchParams.get("prompt");

  useEffect(() => {
    if (categoryId === "presentations") {
      router.replace("/dashboard/new");
    }
    if (categoryId === "news-photocards") {
      router.replace("/dashboard/generate/news-photocard" as Route);
    }
  }, [categoryId, router]);

  if (!category) {
    return (
      <div className="panel">
        <p className="text-sm text-slate-300">Category not found.</p>
        <Link href="/dashboard" className="mt-3 inline-block text-sm text-cyan-300 hover:underline">
          Back to marketplace
        </Link>
      </div>
    );
  }

  if (categoryId === "presentations") {
    return <p className="text-sm text-slate-400">Redirecting to presentation generator…</p>;
  }

  if (categoryId === "news-photocards") {
    return <p className="text-sm text-slate-400">Redirecting to news photocard generator…</p>;
  }

  const Icon = categoryIcon(category.icon);

  return (
    <div className="space-y-6">
      <Link href="/dashboard" className="inline-flex items-center gap-1 text-xs text-slate-400 hover:text-white">
        <ArrowLeft className="h-3.5 w-3.5" /> Marketplace
      </Link>

      <section className="panel">
        <div className={`flex items-center gap-4 rounded-xl bg-gradient-to-r ${category.gradient} p-6`}>
          <div className="rounded-xl bg-black/25 p-3">
            <Icon className="h-8 w-8 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-white">{category.name}</h1>
            <p className="mt-1 text-sm text-white/85">{category.description}</p>
          </div>
        </div>
      </section>

      <section className="panel border-amber-400/20 bg-amber-400/5">
        <p className="text-sm font-medium text-amber-100">Studio generation temporarily unavailable</p>
        <p className="mt-2 text-sm text-slate-300">
          This category is listed in the marketplace for browsing. AI design generation and the visual editor are
          disabled while we stabilize the core app.
        </p>
        {prompt ? (
          <p className="mt-3 rounded-lg border border-white/10 bg-slate-950/50 p-3 text-xs text-slate-400">
            Your prompt: {prompt}
          </p>
        ) : null}
        <div className="mt-4 flex flex-wrap gap-2">
          <Link href="/dashboard/new">
            <Button size="sm">
              <Presentation className="h-4 w-4" /> Use PPT generator
            </Button>
          </Link>
          <Link href="/dashboard">
            <Button size="sm" variant="secondary">
              Back to marketplace
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
