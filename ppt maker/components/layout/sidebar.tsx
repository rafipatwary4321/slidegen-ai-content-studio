import Link from "next/link";
import type { Route } from "next";
import { Calendar, History, LayoutGrid, Newspaper, PlusCircle, Sparkles } from "lucide-react";
import type { LucideIcon } from "lucide-react";

const navItems = [
  { href: "/dashboard", label: "Marketplace", icon: LayoutGrid },
  { href: "/dashboard/new", label: "New Presentation", icon: PlusCircle },
  { href: "/dashboard/generate/news-photocard", label: "News Photocard", icon: Newspaper },
  { href: "/dashboard/generate/poster", label: "Poster Generator", icon: Calendar },
  { href: "/dashboard/history", label: "History", icon: History }
] as const satisfies ReadonlyArray<{ href: Route; label: string; icon: LucideIcon }>;

export function Sidebar() {
  return (
    <aside className="glass hidden w-72 shrink-0 rounded-2xl p-4 lg:block">
      <div className="mb-5 rounded-xl border border-white/10 bg-gradient-to-br from-violet-500/15 via-white/[0.03] to-cyan-500/15 p-4">
        <div className="mb-2 flex items-center gap-2">
          <span className="rounded-lg bg-gradient-to-r from-violet-500 to-cyan-400 p-1.5">
            <Sparkles className="h-4 w-4 text-white" />
          </span>
          <span className="text-sm font-semibold text-white">SlideGen AI</span>
        </div>
        <p className="text-xs text-slate-400">Presentation generator + category marketplace.</p>
      </div>

      <nav className="space-y-1.5">
        {navItems.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className="group flex items-center gap-3 rounded-xl border border-transparent px-3 py-2.5 text-sm text-slate-300 transition-all hover:border-white/15 hover:bg-white/10 hover:text-white"
          >
            <Icon className="h-4 w-4 text-slate-400 transition group-hover:text-cyan-200" />
            <span>{label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
}
