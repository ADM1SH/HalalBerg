import type { Metadata } from "next";
import { JetBrains_Mono } from "next/font/google";
import { TerminalShell } from "@/components/layout/TerminalShell";
import "./globals.css";

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
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
    <html lang="en" className={`${jetbrainsMono.variable} h-full antialiased`}>
      <head>
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
        />
      </head>
      <body className="h-full">
        <TerminalShell>{children}</TerminalShell>
      </body>
    </html>
  );
}
