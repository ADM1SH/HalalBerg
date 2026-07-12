"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/portfolio", label: "Portfolio" },
  { href: "/screener", label: "Screener" },
  { href: "/options", label: "Options" },
  { href: "/optimization", label: "Optimization" },
];

export function TopNavBar() {
  const [now, setNow] = useState<Date | null>(null);
  const pathname = usePathname();

  useEffect(() => {
    setNow(new Date());
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <header className="flex h-12 shrink-0 items-center justify-between border-b border-outline-variant bg-surface-container-lowest px-4">
      <div className="flex items-center gap-6">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-sm font-black tracking-tighter text-primary">
            HALAL<span className="text-secondary">BURG</span>
          </span>
          <span className="text-[10px] uppercase tracking-wider text-on-surface-dim">
            Terminal
          </span>
        </Link>
        <nav className="hidden items-center gap-4 text-xs uppercase tracking-wide text-outline md:flex">
          {LINKS.map((link) => {
            const active = link.href === "/" ? pathname === "/" : pathname.startsWith(link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={
                  active
                    ? "border-b-2 border-primary pb-1 text-primary"
                    : "hover:text-secondary"
                }
              >
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>
      <div className="flex items-center gap-4">
        <input
          type="text"
          placeholder="CMD..."
          className="hidden w-56 rounded-none border border-outline bg-surface px-2 py-1 text-xs text-primary placeholder:text-outline focus:border-primary focus:outline-none sm:block"
        />
        <span className="tabular text-xs tracking-widest text-primary">
          {now
            ? `${now.toLocaleTimeString("en-GB", { hour12: false, timeZone: "UTC" })} GMT`
            : "--:--:-- GMT"}
        </span>
      </div>
    </header>
  );
}
