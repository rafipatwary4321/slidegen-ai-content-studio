"use client";

import Link from "next/link";
import { useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import { signUp } from "@/lib/api/client";
import { Button } from "@/components/ui/button";

export default function SignUpPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await signUp(email, password, name || undefined);
      const result = await signIn("credentials", { email, password, redirect: false });
      if (result?.error) {
        setError("Account created, but auto sign in failed. Please sign in manually.");
        setLoading(false);
        return;
      }
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create account.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-hero-gradient px-4">
      <section className="panel w-full max-w-md p-6 sm:p-7">
        <p className="text-xs uppercase tracking-[0.16em] text-slate-400">SlideGen AI</p>
        <h1 className="mt-2 text-2xl font-semibold text-white">Create account</h1>
        <p className="mt-2 text-sm text-slate-300">Start generating investor-ready decks in minutes.</p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-3">
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Name (optional)"
            className="w-full rounded-xl border border-white/15 bg-slate-900/70 px-3 py-2 text-sm text-white outline-none ring-cyan-300/40 transition focus:ring"
          />
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
            minLength={6}
            required
          />
          {error ? <p className="text-xs text-red-300">{error}</p> : null}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Creating account..." : "Create account"}
          </Button>
        </form>

        <p className="mt-4 text-xs text-slate-400">
          Already have an account? <Link href="/auth/signin" className="text-cyan-300 hover:text-cyan-200">Sign in</Link>
        </p>
      </section>
    </main>
  );
}
