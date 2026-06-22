import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Nexus AI — Your AI-Powered Workspace",
  description:
    "An AI-powered productivity ecosystem combining chat, notes, tasks, finance, trading, and automation.",
  keywords: [
    "AI",
    "productivity",
    "workspace",
    "notes",
    "tasks",
    "finance",
    "trading",
    "automation",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-primary font-sans">{children}</body>
    </html>
  );
}
