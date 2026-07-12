import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { TerminalShell } from "@/components/layout/TerminalShell";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "HalalBurg Terminal",
  description: "Shariah-compliant financial analysis and portfolio terminal",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="h-full">
        <TerminalShell>{children}</TerminalShell>
      </body>
    </html>
  );
}
