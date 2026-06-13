import Link from "next/link";
import type { Route } from "next";
import { ArrowLeft } from "lucide-react";
import { PageHeader } from "@/components/ui/page-header";
import { ErrorBanner } from "@/components/ui/inline-feedback";

interface GeneratorShellProps {
  backHref?: Route;
  backLabel?: string;
  eyebrow: string;
  title: string;
  description: string;
  accent?: "cyan" | "violet";
  error?: string | null;
  children: React.ReactNode;
}

const accentRing: Record<NonNullable<GeneratorShellProps["accent"]>, string> = {
  cyan: "from-cyan-500/20 via-transparent to-violet-500/10",
  violet: "from-violet-500/20 via-transparent to-cyan-500/10"
};

export function GeneratorShell({
  backHref = "/dashboard",
  backLabel = "Marketplace",
  eyebrow,
  title,
  description,
  accent = "cyan",
  error,
  children
}: GeneratorShellProps) {
  return (
    <div className="space-y-6 pb-12">
      <Link href={backHref} className="studio-back-link">
        <ArrowLeft className="h-3.5 w-3.5" />
        {backLabel}
      </Link>

      <div className={`studio-generator-hero bg-gradient-to-br ${accentRing[accent]}`}>
        <PageHeader eyebrow={eyebrow} title={title} description={description} />
      </div>

      {error ? <ErrorBanner message={error} /> : null}

      {children}
    </div>
  );
}
