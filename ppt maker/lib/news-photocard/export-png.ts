/**
 * Real PNG export via HTML Canvas — renders the same layout as the live preview
 * at production dimensions (1080px wide).
 */

import { EXPORT_DIMENSIONS, type PhotocardRenderModel } from "@/lib/news-photocard/render-model";
import type { NewsToneId } from "@/lib/news-photocard/types";

interface ToneLayout {
  strip: boolean;
  badgeRadius: number;
  headlineSize: number;
  subheadSize: number;
}

const TONE_LAYOUT: Record<NewsToneId, ToneLayout> = {
  "breaking-news": { strip: true, badgeRadius: 4, headlineSize: 72, subheadSize: 30 },
  "premium-editorial": { strip: false, badgeRadius: 2, headlineSize: 64, subheadSize: 28 },
  "youth-media": { strip: true, badgeRadius: 999, headlineSize: 68, subheadSize: 30 },
  "corporate-press": { strip: false, badgeRadius: 6, headlineSize: 58, subheadSize: 26 }
};

function loadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error("Failed to load image for export."));
    img.src = src;
  });
}

async function ensureFonts(language: PhotocardRenderModel["language"]): Promise<void> {
  if (language === "bn") {
    await document.fonts.load('700 64px "Noto Sans Bengali"');
    await document.fonts.load('400 32px "Noto Sans Bengali"');
  } else {
    await document.fonts.load("700 64px Georgia");
    await document.fonts.load("400 32px sans-serif");
  }
  await document.fonts.ready;
}

function headlineFont(language: PhotocardRenderModel["language"]): string {
  return language === "bn" ? "700 64px 'Noto Sans Bengali', sans-serif" : "700 64px Georgia, 'Times New Roman', serif";
}

function bodyFont(language: PhotocardRenderModel["language"]): string {
  return language === "bn" ? "400 32px 'Noto Sans Bengali', sans-serif" : "400 32px Inter, system-ui, sans-serif";
}

function wrapText(ctx: CanvasRenderingContext2D, text: string, x: number, y: number, maxWidth: number, lineHeight: number): number {
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

export async function renderPhotocardToCanvas(model: PhotocardRenderModel): Promise<HTMLCanvasElement> {
  await ensureFonts(model.language);

  const { width, height } = EXPORT_DIMENSIONS[model.aspectRatio];
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    throw new Error("Canvas is not supported in this browser.");
  }

  const { palette } = model;
  const layout = TONE_LAYOUT[model.tone];
  const pad = Math.round(width * 0.06);
  const contentW = width - pad * 2;

  ctx.fillStyle = palette.bg;
  ctx.fillRect(0, 0, width, height);

  if (layout.strip) {
    ctx.fillStyle = palette.accent;
    ctx.fillRect(0, 0, width, Math.round(height * 0.03));
  } else {
    ctx.fillStyle = palette.gold;
    ctx.fillRect(pad, Math.round(height * 0.04), contentW, 2);
  }

  const headerY = layout.strip ? Math.round(height * 0.06) : Math.round(height * 0.07);

  ctx.font = `700 ${Math.round(width * 0.028)}px ${model.language === "bn" ? "'Noto Sans Bengali'" : "sans-serif"}`;
  const badgeText = model.category.toUpperCase();
  const badgePadX = 18;
  const badgePadY = 10;
  const badgeW = ctx.measureText(badgeText).width + badgePadX * 2;
  const badgeH = Math.round(width * 0.05);
  drawRoundedRect(ctx, pad, headerY, badgeW, badgeH, layout.badgeRadius, palette.badge);
  ctx.fillStyle = palette.text;
  ctx.textBaseline = "middle";
  ctx.fillText(badgeText, pad + badgePadX, headerY + badgeH / 2);

  const logoSize = Math.round(width * 0.1);
  const logoX = width - pad - logoSize;
  if (model.logoObjectUrl) {
    try {
      const logo = await loadImage(model.logoObjectUrl);
      ctx.drawImage(logo, logoX, headerY, logoSize, logoSize);
    } catch {
      drawLogoPlaceholder(ctx, logoX, headerY, logoSize, palette.muted);
    }
  } else {
    drawLogoPlaceholder(ctx, logoX, headerY, logoSize, palette.muted);
  }

  const headlineY = Math.round(height * 0.16);
  ctx.fillStyle = palette.text;
  ctx.font = headlineFont(model.language).replace("64px", `${layout.headlineSize}px`);
  ctx.textBaseline = "top";
  const subheadStart = wrapText(ctx, model.headline, pad, headlineY, contentW, layout.headlineSize * 1.15);

  if (model.subheadline) {
    ctx.fillStyle = palette.muted;
    ctx.font = bodyFont(model.language).replace("32px", `${layout.subheadSize}px`);
    wrapText(ctx, model.subheadline, pad, subheadStart + 16, contentW, layout.subheadSize * 1.35);
  }

  const heroY = Math.round(height * 0.58);
  const heroH = Math.round(height * (model.aspectRatio === "9:16" ? 0.24 : 0.2));
  drawRoundedRect(ctx, pad, heroY, contentW, heroH, 12, palette.surface);
  ctx.strokeStyle = `${palette.muted}44`;
  ctx.lineWidth = 2;
  ctx.stroke();

  if (model.imageObjectUrl) {
    try {
      const hero = await loadImage(model.imageObjectUrl);
      ctx.save();
      drawRoundedRect(ctx, pad, heroY, contentW, heroH, 12, palette.surface);
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

  const footerY = height - Math.round(height * 0.08);
  ctx.strokeStyle = `${palette.muted}33`;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pad, footerY);
  ctx.lineTo(width - pad, footerY);
  ctx.stroke();

  ctx.fillStyle = palette.gold;
  ctx.font = bodyFont(model.language).replace("32px", `${Math.round(layout.subheadSize * 0.85)}px`);
  ctx.textBaseline = "top";
  ctx.fillText(model.dateStr, pad, footerY + 14);

  ctx.fillStyle = palette.muted;
  ctx.textAlign = "right";
  ctx.font = `600 ${Math.round(layout.subheadSize * 0.75)}px sans-serif`;
  ctx.fillText("SLIDEGEN NEWS", width - pad, footerY + 16);
  ctx.textAlign = "left";

  return canvas;
}

function drawLogoPlaceholder(ctx: CanvasRenderingContext2D, x: number, y: number, size: number, color: string) {
  ctx.strokeStyle = `${color}66`;
  ctx.lineWidth = 2;
  ctx.setLineDash([6, 4]);
  ctx.strokeRect(x, y, size, size);
  ctx.setLineDash([]);
  ctx.fillStyle = color;
  ctx.font = `600 ${Math.round(size * 0.22)}px sans-serif`;
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
  ctx.font = `600 ${Math.round(h * 0.12)}px sans-serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("HERO IMAGE", x + w / 2, y + h / 2);
  ctx.textAlign = "left";
  ctx.textBaseline = "alphabetic";
}

export async function exportNewsPhotocardPng(model: PhotocardRenderModel): Promise<Blob> {
  const canvas = await renderPhotocardToCanvas(model);
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

export function downloadPngBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}
