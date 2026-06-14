/**
 * Real PNG export via HTML Canvas — poster layout at production width (1080px).
 */

import { downloadPngBlob } from "@/lib/news-photocard/export-png";
import { EXPORT_DIMENSIONS, type PosterRenderModel } from "@/lib/poster/render-model";
import type { PosterDesignToneId } from "@/lib/poster/types";

interface ToneLayout {
  accentBar: boolean;
  goldRule: boolean;
  gradient: boolean;
  titleSize: number;
  subSize: number;
  metaSize: number;
}

const TONE_LAYOUT: Record<PosterDesignToneId, ToneLayout> = {
  "premium-corporate": { accentBar: false, goldRule: false, gradient: false, titleSize: 64, subSize: 28, metaSize: 22 },
  "bold-political": { accentBar: true, goldRule: false, gradient: false, titleSize: 72, subSize: 28, metaSize: 22 },
  "modern-youth": { accentBar: true, goldRule: false, gradient: true, titleSize: 68, subSize: 30, metaSize: 24 },
  "academic-clean": { accentBar: false, goldRule: false, gradient: false, titleSize: 58, subSize: 26, metaSize: 22 },
  "luxury-event": { accentBar: false, goldRule: true, gradient: false, titleSize: 62, subSize: 28, metaSize: 22 }
};

function loadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error("Failed to load image for export."));
    img.src = src;
  });
}

async function ensureFonts(language: PosterRenderModel["language"]): Promise<void> {
  if (language === "bn") {
    await document.fonts.load('700 64px "Noto Sans Bengali"');
    await document.fonts.load('400 28px "Noto Sans Bengali"');
  } else {
    await document.fonts.load("700 64px Georgia");
    await document.fonts.load("400 28px sans-serif");
  }
  await document.fonts.ready;
}

function titleFont(language: PosterRenderModel["language"], size: number): string {
  const family = language === "bn" ? "'Noto Sans Bengali', sans-serif" : "Georgia, 'Times New Roman', serif";
  return `700 ${size}px ${family}`;
}

function bodyFont(language: PosterRenderModel["language"], size: number): string {
  const family = language === "bn" ? "'Noto Sans Bengali', sans-serif" : "Inter, system-ui, sans-serif";
  return `400 ${size}px ${family}`;
}

function wrapText(
  ctx: CanvasRenderingContext2D,
  text: string,
  x: number,
  y: number,
  maxWidth: number,
  lineHeight: number
): number {
  const words = text.split(/\s+/);
  let line = "";
  let cursorY = y;
  for (let i = 0; i < words.length; i++) {
    const test = line ? `${line} ${words[i]}` : words[i];
    if (ctx.measureText(test).width > maxWidth && line) {
      ctx.fillText(line, x, cursorY);
      line = words[i];
      cursorY += lineHeight;
    } else {
      line = test;
    }
  }
  if (line) {
    ctx.fillText(line, x, cursorY);
    cursorY += lineHeight;
  }
  return cursorY;
}

function drawRoundedRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  r: number,
  fill: string
) {
  const radius = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.arcTo(x + w, y, x + w, y + h, radius);
  ctx.arcTo(x + w, y + h, x, y + h, radius);
  ctx.arcTo(x, y + h, x, y, radius);
  ctx.arcTo(x, y, x + w, y, radius);
  ctx.closePath();
  ctx.fillStyle = fill;
  ctx.fill();
}

function drawGradientBar(ctx: CanvasRenderingContext2D, width: number, height: number) {
  const grad = ctx.createLinearGradient(0, 0, width, 0);
  grad.addColorStop(0, "#d946ef");
  grad.addColorStop(0.5, "#8b5cf6");
  grad.addColorStop(1, "#22d3ee");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, width, height);
}

export async function renderPosterToCanvas(model: PosterRenderModel): Promise<HTMLCanvasElement> {
  await ensureFonts(model.language);

  const { width, height } = EXPORT_DIMENSIONS[model.aspectRatio];
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("Canvas is not supported in this browser.");

  const { palette } = model;
  const layout = TONE_LAYOUT[model.designTone];
  const pad = Math.round(width * 0.08);
  const contentW = width - pad * 2;
  const isLight = model.designTone === "academic-clean";

  ctx.fillStyle = palette.bg;
  ctx.fillRect(0, 0, width, height);

  let contentStartY = pad;
  if (layout.gradient) {
    drawGradientBar(ctx, width, Math.round(height * 0.025));
    contentStartY = Math.round(height * 0.05);
  } else if (layout.accentBar) {
    ctx.fillStyle = palette.accent;
    ctx.fillRect(0, 0, width, Math.round(height * 0.025));
    contentStartY = Math.round(height * 0.05);
  } else if (layout.goldRule) {
    ctx.fillStyle = palette.accent;
    ctx.fillRect(pad, Math.round(height * 0.04), contentW, 2);
    contentStartY = Math.round(height * 0.06);
  }

  ctx.font = `700 ${Math.round(width * 0.026)}px sans-serif`;
  const badge = model.posterTypeLabel.toUpperCase();
  const badgeW = ctx.measureText(badge).width + 36;
  const badgeH = Math.round(width * 0.045);
  drawRoundedRect(ctx, pad, contentStartY, badgeW, badgeH, 6, `${palette.accent}33`);
  ctx.fillStyle = palette.accent;
  ctx.textBaseline = "middle";
  ctx.fillText(badge, pad + 18, contentStartY + badgeH / 2);

  const logoSize = Math.round(width * 0.1);
  const logoX = width - pad - logoSize;
  if (model.logoObjectUrl) {
    try {
      const logo = await loadImage(model.logoObjectUrl);
      ctx.drawImage(logo, logoX, contentStartY, logoSize, logoSize);
    } catch {
      drawLogoPlaceholder(ctx, logoX, contentStartY, logoSize, palette.muted);
    }
  } else {
    drawLogoPlaceholder(ctx, logoX, contentStartY, logoSize, palette.muted);
  }

  const titleY = contentStartY + badgeH + Math.round(height * 0.04);
  ctx.fillStyle = palette.text;
  ctx.font = titleFont(model.language, layout.titleSize);
  ctx.textBaseline = "top";
  let cursorY = wrapText(ctx, model.title, pad, titleY, contentW, layout.titleSize * 1.12);

  if (model.subtitle) {
    ctx.fillStyle = palette.muted;
    ctx.font = bodyFont(model.language, layout.subSize);
    cursorY = wrapText(ctx, model.subtitle, pad, cursorY + 12, contentW, layout.subSize * 1.3);
  }

  const heroY = cursorY + Math.round(height * 0.04);
  const heroH = Math.round(height * (model.aspectRatio === "9:16" ? 0.22 : model.aspectRatio === "A4" ? 0.18 : 0.2));
  drawRoundedRect(ctx, pad, heroY, contentW, heroH, 14, palette.surface);
  ctx.strokeStyle = `${palette.muted}44`;
  ctx.lineWidth = 2;
  ctx.stroke();

  if (model.imageObjectUrl) {
    try {
      const hero = await loadImage(model.imageObjectUrl);
      ctx.save();
      drawRoundedRect(ctx, pad, heroY, contentW, heroH, 14, palette.surface);
      ctx.clip();
      const scale = Math.max(contentW / hero.width, heroH / hero.height);
      const drawW = hero.width * scale;
      const drawH = hero.height * scale;
      ctx.drawImage(hero, pad + (contentW - drawW) / 2, heroY + (heroH - drawH) / 2, drawW, drawH);
      ctx.restore();
    } catch {
      drawHeroPlaceholder(ctx, pad, heroY, contentW, heroH, palette.muted);
    }
  } else {
    drawHeroPlaceholder(ctx, pad, heroY, contentW, heroH, palette.muted);
  }

  let metaY = heroY + heroH + Math.round(height * 0.03);
  ctx.font = bodyFont(model.language, layout.metaSize);
  ctx.textBaseline = "top";

  if (model.dateTime) {
    ctx.fillStyle = palette.muted;
    metaY = wrapText(ctx, model.dateTime, pad, metaY, contentW, layout.metaSize * 1.4);
    metaY += 4;
  }
  if (model.venue) {
    ctx.fillStyle = palette.muted;
    metaY = wrapText(ctx, model.venue, pad, metaY, contentW, layout.metaSize * 1.4);
    metaY += 4;
  }
  if (model.organizer) {
    ctx.fillStyle = palette.muted;
    metaY = wrapText(ctx, model.organizer, pad, metaY, contentW, layout.metaSize * 1.4);
  }

  const ctaText = model.ctaText || "Learn More";
  ctx.font = `700 ${Math.round(layout.metaSize * 0.95)}px sans-serif`;
  const ctaPadX = 28;
  const ctaW = ctx.measureText(ctaText.toUpperCase()).width + ctaPadX * 2;
  const ctaH = Math.round(width * 0.055);
  const ctaY = height - pad - ctaH;
  drawRoundedRect(ctx, pad, ctaY, ctaW, ctaH, 12, palette.cta);
  ctx.fillStyle = isLight ? "#ffffff" : palette.bg;
  ctx.textBaseline = "middle";
  ctx.fillText(ctaText.toUpperCase(), pad + ctaPadX, ctaY + ctaH / 2);

  return canvas;
}

function drawLogoPlaceholder(ctx: CanvasRenderingContext2D, x: number, y: number, size: number, color: string) {
  ctx.strokeStyle = `${color}66`;
  ctx.lineWidth = 2;
  ctx.setLineDash([6, 4]);
  ctx.strokeRect(x, y, size, size);
  ctx.setLineDash([]);
  ctx.fillStyle = color;
  ctx.font = `600 ${Math.round(size * 0.2)}px sans-serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("LOGO", x + size / 2, y + size / 2);
  ctx.textAlign = "left";
  ctx.textBaseline = "alphabetic";
}

function drawHeroPlaceholder(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  color: string
) {
  ctx.fillStyle = color;
  ctx.font = `600 ${Math.round(h * 0.1)}px sans-serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("HERO IMAGE", x + w / 2, y + h / 2);
  ctx.textAlign = "left";
  ctx.textBaseline = "alphabetic";
}

export async function exportPosterPng(model: PosterRenderModel): Promise<Blob> {
  const canvas = await renderPosterToCanvas(model);
  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => {
        if (blob) resolve(blob);
        else reject(new Error("Failed to encode PNG."));
      },
      "image/png",
      1
    );
  });
}

export { downloadPngBlob };
