import type { Metadata } from "next";
import "./globals.css";
import { AppSessionProvider } from "@/components/providers/session-provider";

export const metadata: Metadata = {
  title: "SlideGen AI — Universal AI-Powered PPT Generator",
  description: "Upload documents, generate AI slide outlines, and export native PowerPoint decks."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppSessionProvider>{children}</AppSessionProvider>
      </body>
    </html>
  );
}
