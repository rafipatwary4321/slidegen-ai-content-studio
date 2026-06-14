import Link from "next/link";
import { ArrowLeft, LayoutGrid } from "lucide-react";
import { Button } from "@/components/ui/button";

const quickLinks = [
  { href: "/", label: "Home" },
  { href: "/dashboard", label: "Marketplace" },
  { href: "/dashboard/new", label: "New Presentation" },
  { href: "/dashboard/history", label: "History" },
  { href: "/dashboard/generate/news-photocard", label: "News Photocard" },
  { href: "/dashboard/generate/poster", label: "Poster Generator" }
] as const;

export default function NotFound() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-4">
      <div className="panel max-w-lg text-center">
        <p className="text-xs uppercase tracking-[0.2em] text-slate-500">404</p>
        <h1 className="mt-2 text-2xl font-semibold text-white">Page not found</h1>
        <p className="mt-3 text-sm text-slate-400">
          This URL does not exist in SlideGen AI. Use one of the working routes below.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-2">
          {quickLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="rounded-lg border border-white/10 bg-white/[0.04] px-3 py-1.5 text-xs text-slate-300 transition hover:border-white/20 hover:text-white"
            >
              {link.label}
            </Link>
          ))}
        </div>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <Link href="/dashboard">
            <Button size="sm">
              <LayoutGrid className="h-4 w-4" /> Open marketplace
            </Button>
          </Link>
          <Link href="/">
            <Button size="sm" variant="secondary">
              <ArrowLeft className="h-4 w-4" /> Back home
            </Button>
          </Link>
        </div>
      </div>
    </main>
  );
}
