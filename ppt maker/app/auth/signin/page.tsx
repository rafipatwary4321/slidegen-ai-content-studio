"use client";

import Link from "next/link";
import { useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

export default function SignInPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);

    const result = await signIn("credentials", {
      email,
      password,
      redirect: false
    });

    setLoading(false);

    if (result?.error) {
      setError("Invalid email or password.");
      return;
    }

    router.push("/dashboard");
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-hero-gradient px-4">
      <section className="panel w-full max-w-md p-6 sm:p-7">
        <p className="text-xs uppercase tracking-[0.16em] text-slate-400">SlideGen AI</p>
        <h1 className="mt-2 text-2xl font-semibold text-white">Welcome back</h1>
        <p className="mt-2 text-sm text-slate-300">Sign in to continue building premium AI presentations.</p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-3">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            className="w-full rounded-xl border border-white/15 bg-slate-900/70 px-3 py-2 text-sm text-white outline-none ring-cyan-300/40 transition focus:ring"
            required
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="w-full rounded-xl border border-white/15 bg-slate-900/70 px-3 py-2 text-sm text-white outline-none ring-cyan-300/40 transition focus:ring"
            required
          />
          {error ? <p className="text-xs text-red-300">{error}</p> : null}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Signing in..." : "Sign in"}
          </Button>
        </form>

        <p className="mt-4 text-xs text-slate-400">
          No account yet? <Link href="/auth/signup" className="text-cyan-300 hover:text-cyan-200">Create one</Link>
        </p>
      </section>
    </main>
  );
}
