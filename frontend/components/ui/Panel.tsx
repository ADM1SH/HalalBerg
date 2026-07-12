import type { ReactNode } from "react";

interface PanelProps {
  title: string;
  accessory?: ReactNode;
  children: ReactNode;
  className?: string;
  bodyClassName?: string;
}

export function Panel({
  title,
  accessory,
  children,
  className = "",
  bodyClassName = "",
}: PanelProps) {
  return (
    <section
      className={`flex flex-col overflow-hidden rounded-sm border border-outline-variant bg-surface ${className}`}
    >
      <header className="flex shrink-0 items-center justify-between border-b border-outline-variant bg-surface-container-lowest px-3 py-1.5">
        <h2 className="text-[11px] font-semibold uppercase tracking-wider text-on-surface-dim">
          {title}
        </h2>
        {accessory}
      </header>
      <div className={`min-h-0 flex-1 overflow-auto ${bodyClassName}`}>
        {children}
      </div>
    </section>
  );
}
