"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const ITEMS = [
  { href: "/", label: "DASH", title: "Dashboard" },
  { href: "/portfolio", label: "PORT", title: "Portfolio" },
  { href: "/screener", label: "EQS", title: "Equity Screener" },
  { href: "/options", label: "OPT", title: "Options" },
  { href: "/optimization", label: "OPTM", title: "Optimization" },
];

export function SideNavBar() {
  const pathname = usePathname();

  return (
    <aside className="flex w-16 shrink-0 flex-col items-center gap-1 border-r border-outline-variant bg-surface-container-lowest py-3">
      {ITEMS.map((item) => {
        const active =
          item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
        return (
          <Link
            key={item.href}
            href={item.href}
            title={item.title}
            className={`flex h-12 w-12 flex-col items-center justify-center rounded-sm text-[10px] font-semibold tracking-wide transition-colors ${
              active
                ? "bg-surface-container-high text-primary"
                : "text-on-surface-dim hover:bg-surface-container hover:text-on-surface"
            }`}
          >
            {item.label}
          </Link>
        );
      })}
    </aside>
  );
}
