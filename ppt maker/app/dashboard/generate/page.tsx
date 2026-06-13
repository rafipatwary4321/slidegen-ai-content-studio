import Link from "next/link";
import type { Route } from "next";
import { Calendar, Newspaper } from "lucide-react";
import { PageHeader } from "@/components/ui/page-header";

const generators = [
  {
    href: "/dashboard/generate/news-photocard" as Route,
    title: "News Photocard",
    description: "Editorial news cards with headline, category badge, and theme.",
    icon: Newspaper
  },
  {
    href: "/dashboard/generate/poster" as Route,
    title: "Poster Generator",
    description: "Event, political, educational, and promotional posters.",
    icon: Calendar
  }
] as const;

export default function GenerateHubPage() {
  return (
    <div className="space-y-6 pb-10">
      <PageHeader
        eyebrow="Content Studio"
        title="Content Generators"
        description="Choose a generator to create news photocards or posters."
      />

      <div className="grid gap-4 sm:grid-cols-2">
        {generators.map(({ href, title, description, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className="panel group transition hover:border-white/20 hover:bg-white/[0.06]"
          >
            <div className="flex items-start gap-4">
              <span className="rounded-xl bg-cyan-500/15 p-3 text-cyan-300">
                <Icon className="h-5 w-5" />
              </span>
              <div>
                <h2 className="text-base font-semibold text-white group-hover:text-cyan-100">{title}</h2>
                <p className="mt-1.5 text-sm text-slate-400">{description}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
