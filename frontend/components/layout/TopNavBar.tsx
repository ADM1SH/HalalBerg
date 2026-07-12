"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export function TopNavBar() {
  const [now, setNow] = useState<Date | null>(null);

  useEffect(() => {
    setNow(new Date());
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <header className="flex h-12 shrink-0 items-center justify-between border-b border-outline-variant bg-surface-container-lowest px-4">
      <div className="flex items-center gap-6">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-sm font-bold tracking-widest text-primary">
            HALAL<span className="text-secondary">BURG</span>
          </span>
          <span className="text-[10px] uppercase tracking-wider text-on-surface-dim">
            Terminal
          </span>
        </Link>
        <nav className="hidden items-center gap-4 text-xs uppercase tracking-wide text-on-surface-dim md:flex">
          <Link href="/" className="hover:text-primary">
            Dashboard
          </Link>
          <Link href="/portfolio" className="hover:text-primary">
            Portfolio
          </Link>
          <Link href="/screener" className="hover:text-primary">
            Screener
          </Link>
          <Link href="/options" className="hover:text-primary">
            Options
          </Link>
          <Link href="/optimization" className="hover:text-primary">
            Optimization
          </Link>
        </nav>
      </div>
      <div className="flex items-center gap-4">
        <input
          type="text"
          placeholder="Search ticker / command..."
          className="hidden w-56 rounded-sm border border-outline bg-surface px-2 py-1 text-xs text-on-surface placeholder:text-on-surface-dim focus:border-primary focus:outline-none sm:block"
        />
        <span className="tabular text-xs text-on-surface-dim">
          {now
            ? now.toLocaleTimeString("en-GB", { hour12: false })
            : "--:--:--"}
        </span>
      </div>
    </header>
  );
}
