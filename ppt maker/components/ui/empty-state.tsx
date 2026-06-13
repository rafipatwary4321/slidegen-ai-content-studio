import { Inbox } from "lucide-react";

interface EmptyStateProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
}

export function EmptyState({ title, description, icon }: EmptyStateProps) {
  return (
    <div className="panel flex flex-col items-center justify-center px-6 py-10 text-center">
      <div className="mb-3 rounded-xl border border-white/15 bg-white/10 p-2.5 text-cyan-200">{icon ?? <Inbox className="h-5 w-5" />}</div>
      <h3 className="text-base font-semibold text-white">{title}</h3>
      <p className="mt-2 max-w-md text-sm text-slate-400">{description}</p>
    </div>
  );
}
