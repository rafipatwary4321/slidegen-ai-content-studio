import { Suspense } from "react";
import { CategoryWorkspace } from "@/components/studio/category-workspace";

export default function StudioCategoryPage({ params }: { params: { categoryId: string } }) {
  return (
    <Suspense fallback={<div className="panel text-sm text-slate-400">Loading workspace…</div>}>
      <CategoryWorkspace categoryId={params.categoryId} />
    </Suspense>
  );
}
