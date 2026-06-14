import Link from "next/link";
import { PageHeader } from "@/components/ui/page-header";
import { Button } from "@/components/ui/button";

export default function DashboardNotFound() {
  return (
    <div className="space-y-6 pb-10">
      <PageHeader
        eyebrow="404"
        title="Dashboard page not found"
        description="This dashboard route does not exist. Return to a working page below."
      />
      <div className="panel flex flex-wrap gap-3">
        <Link href="/dashboard">
          <Button size="sm">Marketplace</Button>
        </Link>
        <Link href="/dashboard/new">
          <Button size="sm" variant="secondary">
            New Presentation
          </Button>
        </Link>
        <Link href="/dashboard/generate/news-photocard">
          <Button size="sm" variant="secondary">
            News Photocard
          </Button>
        </Link>
        <Link href="/dashboard/generate/poster">
          <Button size="sm" variant="secondary">
            Poster Generator
          </Button>
        </Link>
      </div>
    </div>
  );
}
