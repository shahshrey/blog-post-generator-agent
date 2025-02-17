import type { Metadata } from "next";
import "./globals.css";
import { Toaster } from 'sonner'

export const metadata: Metadata = {
  title: "Blog Post Generator",
  description: "An AI-powered blog post generator built with Next.js and CopilotKit",
  keywords: "blog, AI, writing, content generation",
  authors: [{ name: "Blog Post Generator" }],
  viewport: "width=device-width, initial-scale=1",
  robots: "index, follow",
  themeColor: "#0070f3"
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
        <Toaster richColors position="top-right" />
      </body>
    </html>
  );
}
