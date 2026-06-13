import { AlertTriangle } from "lucide-react";

export function ErrorBanner({ message }: { message: string }) {
  return (
    <div className="panel border-red-300/30 bg-red-500/10 text-red-100">
      <div className="flex items-start gap-2">
        <AlertTriangle className="mt-0.5 h-4 w-4" />
        <p className="text-sm">{message}</p>
      </div>
    </div>
  );
}

export function LoadingCardGrid({ count = 2 }: { count?: number }) {
  return (
    <div className="grid gap-5 lg:grid-cols-2">
      {Array.from({ length: count }).map((_, idx) => (
        <div key={idx} className="panel h-44 animate-pulse bg-white/5" />
      ))}
    </div>
  );
}
