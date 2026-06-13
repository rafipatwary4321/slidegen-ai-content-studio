import { ButtonHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

type Variant = "primary" | "secondary" | "ghost";
type Size = "md" | "sm" | "lg";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
}

const variants: Record<Variant, string> = {
  primary:
    "bg-gradient-to-r from-violet-500 via-indigo-500 to-cyan-500 text-white shadow-[0_0_0_1px_rgba(167,139,250,0.45),0_14px_30px_rgba(14,116,144,0.35)] hover:brightness-110",
  secondary:
    "border border-white/15 bg-white/[0.06] text-slate-200 hover:border-white/25 hover:bg-white/[0.1]",
  ghost: "bg-transparent text-slate-300 hover:bg-white/10 hover:text-white"
};

const sizes: Record<Size, string> = {
  sm: "h-9 px-4 text-xs",
  md: "h-11 px-5 text-sm",
  lg: "h-12 px-6 text-sm"
};

export function Button({ className, variant = "primary", size = "md", ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-xl font-semibold transition-all duration-200 disabled:cursor-not-allowed disabled:opacity-60",
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    />
  );
}
