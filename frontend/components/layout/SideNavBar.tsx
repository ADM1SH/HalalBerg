"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const ITEMS = [
  { href: "/", label: "DASH", title: "Dashboard", icon: "dashboard" },
  { href: "/portfolio", label: "PORT", title: "Portfolio", icon: "account_balance_wallet" },
  { href: "/screener", label: "EQS", title: "Equity Screener", icon: "query_stats" },
  { href: "/options", label: "OPT", title: "Options", icon: "settings_input_component" },
  { href: "/optimization", label: "OPTM", title: "Optimization", icon: "analytics" },
];

export function SideNavBar() {
  const pathname = usePathname();

  return (
    <aside className="flex w-16 shrink-0 flex-col items-center gap-1 border-r border-outline-variant bg-surface-container-lowest py-4">
      <div className="mb-4 flex flex-col items-center gap-1 text-primary">
        <span className="material-symbols-outlined text-2xl">terminal</span>
        <span className="text-[8px] font-bold tracking-wide">HB_TERM</span>
      </div>
      {ITEMS.map((item) => {
        const active =
          item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
        return (
          <Link
            key={item.href}
            href={item.href}
            title={item.title}
            className={`flex h-12 w-14 flex-col items-center justify-center gap-1 text-[9px] font-semibold tracking-wide transition-colors ${
              active
                ? "border-l-2 border-primary bg-primary/10 text-primary"
                : "text-outline hover:bg-surface-container hover:text-secondary"
            }`}
          >
            <span className="material-symbols-outlined text-[20px]">{item.icon}</span>
            {item.label}
          </Link>
        );
      })}
      <div className="mt-auto text-[8px] text-outline">V2.0.4</div>
    </aside>
  );
}
