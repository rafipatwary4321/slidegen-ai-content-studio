import { redirect } from "next/navigation";

export default function PresentationAliasPage({ params }: { params: { id: string } }) {
  redirect(`/dashboard/presentations/${params.id}`);
}
