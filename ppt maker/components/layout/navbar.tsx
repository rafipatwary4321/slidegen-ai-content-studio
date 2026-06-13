import Link from "next/link";
import { Sparkles } from "lucide-react";
import { AuthActions } from "@/components/auth/auth-actions";

export function Navbar() {
  return (
    <header className="sticky top-0 z-30 border-b border-white/10 bg-slate-950/75 backdrop-blur-xl">
      <div className="mx-auto flex h-16 w-full max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex items-center gap-2">
          <span className="rounded-lg bg-gradient-to-r from-violet-500 to-cyan-400 p-1.5">
            <Sparkles className="h-4 w-4 text-white" />
          </span>
          <span className="text-sm font-semibold tracking-wide text-white">SlideGen AI</span>
        </Link>
        <nav className="hidden items-center gap-6 text-sm text-slate-300 md:flex">
          <Link href="#features" className="transition hover:text-white">Features</Link>
          <Link href="#use-cases" className="transition hover:text-white">Use Cases</Link>
          <Link href="/dashboard" className="transition hover:text-white">Dashboard</Link>
        </nav>
        <AuthActions />
      </div>
    </header>
  );
}
