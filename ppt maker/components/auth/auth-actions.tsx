"use client";

import Link from "next/link";
import { signOut, useSession } from "next-auth/react";
import { Button } from "@/components/ui/button";

export function AuthActions() {
  const { data: session, status } = useSession();

  if (status === "loading") {
    return <div className="h-9 w-24 animate-pulse rounded-lg bg-white/10" />;
  }

  if (session?.user) {
    return (
      <div className="flex items-center gap-2">
        <span className="hidden text-xs text-slate-300 sm:inline">{session.user.email}</span>
        <Button size="sm" variant="secondary" onClick={() => signOut({ callbackUrl: "/" })}>
          Sign out
        </Button>
      </div>
    );
  }

  return (
    <Link href="/auth/signin">
      <Button size="sm">Sign in</Button>
    </Link>
  );
}
