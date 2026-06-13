import Link from "next/link";
import { Sparkles } from "lucide-react";
import { AuthActions } from "@/components/auth/auth-actions";
import { Sidebar } from "@/components/layout/sidebar";
import { Button } from "@/components/ui/button";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-950">
      <header className="border-b border-white/10 bg-slate-950/80 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
          <Link href="/" className="flex items-center gap-2 text-sm font-semibold text-white">
            <Sparkles className="h-4 w-4 text-cyan-300" />
            SlideGen AI
          </Link>
          <div className="flex items-center gap-2">
            <Link href="/dashboard/history" className="hidden text-xs text-slate-300 transition hover:text-white sm:inline">
              History
            </Link>
            <Link href="/dashboard/new">
              <Button size="sm">+ New Presentation</Button>
            </Link>
            <AuthActions />
          </div>
        </div>
      </header>
      <div className="mx-auto flex max-w-7xl gap-4 px-4 py-6 sm:gap-6 sm:px-6">
        <Sidebar />
        <main className="min-w-0 flex-1">{children}</main>
      </div>
    </div>
  );
}
