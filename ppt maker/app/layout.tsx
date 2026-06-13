import type { Metadata } from "next";
import { Noto_Sans_Bengali } from "next/font/google";
import "./globals.css";
import { AppSessionProvider } from "@/components/providers/session-provider";

const notoSansBengali = Noto_Sans_Bengali({
  subsets: ["bengali"],
  weight: ["400", "600", "700"],
  variable: "--font-bengali",
  display: "swap"
});

export const metadata: Metadata = {
  title: "SlideGen AI — Universal AI-Powered PPT Generator",
  description: "Upload documents, generate AI slide outlines, and export native PowerPoint decks."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={notoSansBengali.variable}>
      <body className="min-h-screen antialiased">
        <AppSessionProvider>{children}</AppSessionProvider>
      </body>
    </html>
  );
}
