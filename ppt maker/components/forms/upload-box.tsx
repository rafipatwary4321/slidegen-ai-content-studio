"use client";

import { useCallback, useRef, useState } from "react";
import { FileText, Sparkles, UploadCloud } from "lucide-react";
import { Button } from "@/components/ui/button";

const ACCEPT = ".pdf,.docx,.txt";

interface UploadBoxProps {
  selectedFile?: File | null;
  onFileSelect?: (file: File | null) => void;
  disabled?: boolean;
}

function isAllowedFile(file: File): boolean {
  const name = file.name.toLowerCase();
  return name.endsWith(".pdf") || name.endsWith(".docx") || name.endsWith(".txt");
}

export function UploadBox({ selectedFile = null, onFileSelect, disabled = false }: UploadBoxProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const pickFile = useCallback(
    (file: File | null) => {
      if (!file) {
        onFileSelect?.(null);
        return;
      }
      if (!isAllowedFile(file)) {
        return;
      }
      onFileSelect?.(file);
    },
    [onFileSelect]
  );

  function onDrop(event: React.DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setDragging(false);
    if (disabled) return;
    const file = event.dataTransfer.files?.[0];
    if (file) pickFile(file);
  }

  return (
    <section className="panel border-dashed border-white/20 bg-gradient-to-br from-violet-500/10 via-transparent to-cyan-500/10 p-6 sm:p-7">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-semibold text-white">Upload source content</p>
          <p className="mt-1 text-xs text-slate-400">Drag & drop or browse PDF, DOCX, or TXT for AI analysis.</p>
        </div>
        <span className="inline-flex w-fit items-center gap-1 rounded-full border border-white/15 bg-white/10 px-2.5 py-1 text-[11px] text-slate-300">
          <Sparkles className="h-3 w-3" /> AI assisted
        </span>
      </div>

      <div
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") inputRef.current?.click();
        }}
        onDragEnter={(e) => {
          e.preventDefault();
          if (!disabled) setDragging(true);
        }}
        onDragLeave={(e) => {
          e.preventDefault();
          setDragging(false);
        }}
        onDragOver={(e) => e.preventDefault()}
        onDrop={onDrop}
        onClick={() => !disabled && inputRef.current?.click()}
        className={`mt-5 cursor-pointer rounded-2xl border bg-slate-900/70 p-8 text-center transition ${
          dragging
            ? "border-cyan-400/60 bg-cyan-500/10"
            : "border-white/15 hover:border-cyan-300/40 hover:bg-slate-900/80"
        } ${disabled ? "pointer-events-none opacity-60" : ""}`}
      >
        <UploadCloud className={`mx-auto mb-4 h-10 w-10 ${dragging ? "text-cyan-200" : "text-cyan-300"}`} />
        <p className="text-sm font-medium text-white">{dragging ? "Drop file to upload" : "Drop or click to choose a file"}</p>
        <p className="mt-2 text-xs text-slate-400">PDF, DOCX, TXT — max 25MB</p>

        <input
          ref={inputRef}
          type="file"
          className="hidden"
          accept={ACCEPT}
          disabled={disabled}
          onChange={(event) => pickFile(event.target.files?.[0] ?? null)}
        />

        <div className="mt-5 flex flex-wrap items-center justify-center gap-2" onClick={(e) => e.stopPropagation()}>
          <Button
            type="button"
            variant="secondary"
            size="sm"
            disabled={disabled}
            onClick={() => inputRef.current?.click()}
          >
            Browse files
          </Button>
          <span className="inline-flex items-center gap-1 text-xs text-slate-400">
            <FileText className="h-3.5 w-3.5" /> Secure server-side parsing
          </span>
        </div>

        {selectedFile ? (
          <p className="mt-4 text-xs text-cyan-200">
            Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
          </p>
        ) : null}
      </div>
    </section>
  );
}
