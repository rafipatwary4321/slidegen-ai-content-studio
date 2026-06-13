"use client";

import { useState } from "react";
import { Bot, Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { generateContent } from "@/lib/api/client";
import { useEditorStore } from "@/lib/content-studio/editor-store";
import { useStudioStore } from "@/lib/content-studio/store";

export function AiAssistantPanel() {
  const project = useEditorStore((s) => s.project);
  const setProject = useEditorStore((s) => s.setProject);
  const brandKit = useStudioStore((s) => s.brandKit);
  const saveProject = useStudioStore((s) => s.saveProject);
  const [instruction, setInstruction] = useState("");
  const [loading, setLoading] = useState(false);
  const [reply, setReply] = useState<string | null>(null);

  async function handleAssist() {
    if (!project || !instruction.trim()) return;
    setLoading(true);
    setReply(null);
    try {
      const res = await generateContent({
        category_id: project.categoryId,
        prompt: `${project.prompt}\n\nRefine: ${instruction}`,
        aspect_ratio: project.aspectRatio,
        language: project.language,
        workflow: "prompt",
        brand_kit: brandKit
      });
      const merged = { ...res.project, id: project.id, createdAt: project.createdAt };
      setProject(merged);
      saveProject(merged);
      setReply("Design updated with your AI instruction.");
      setInstruction("");
    } catch (e) {
      setReply(e instanceof Error ? e.message : "AI assist failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="border-t border-white/10 p-3">
      <p className="mb-2 flex items-center gap-2 text-[11px] font-medium uppercase tracking-wide text-slate-400">
        <Bot className="h-3.5 w-3.5" /> AI assistant
      </p>
      <textarea
        value={instruction}
        onChange={(e) => setInstruction(e.target.value)}
        rows={3}
        placeholder="e.g. Make headline bolder, add CTA button, use brand colors"
        className="w-full rounded-lg border border-white/10 bg-slate-900 px-2 py-1.5 text-xs text-white outline-none"
      />
      <Button size="sm" className="mt-2 w-full" onClick={handleAssist} disabled={loading || !instruction.trim()}>
        <Send className="h-3.5 w-3.5" /> {loading ? "Applying…" : "Apply with AI"}
      </Button>
      {reply ? <p className="mt-2 text-[11px] text-cyan-200/90">{reply}</p> : null}
    </div>
  );
}
