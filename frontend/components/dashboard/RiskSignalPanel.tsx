"use client";

import { api } from "@/lib/api";
import { usePolling } from "@/lib/usePolling";
import type { RiskSignal } from "@/lib/types";
import { Panel } from "@/components/ui/Panel";

const LEVEL_COLOR: Record<RiskSignal["level"], string> = {
  low: "text-trade-up",
  elevated: "text-trade-neutral",
  high: "text-trade-down",
  critical: "text-trade-down",
};

export function RiskSignalPanel() {
  const { data, error } = usePolling<RiskSignal>(
    (signal) => api.risk(signal) as Promise<RiskSignal>,
    30000
  );

  return (
    <Panel title="Geopolitical Risk Signal" className="h-full">
      {error && <p className="p-3 text-[11px] text-trade-down">{error}</p>}
      {data && (
        <div className="flex h-full flex-col gap-2 p-3 text-[11px]">
          <div className="flex items-baseline gap-2">
            <span className="tabular text-2xl font-semibold text-on-surface">
              {data.escalation_score}
            </span>
            <span className={`uppercase ${LEVEL_COLOR[data.level]}`}>
              {data.level}
            </span>
          </div>
          <div className="flex flex-wrap gap-x-3 gap-y-1 text-on-surface-dim">
            {Object.entries(data.categories).map(([category, count]) => (
              <span key={category}>
                {category} {count}
              </span>
            ))}
          </div>
          <ul className="min-h-0 flex-1 divide-y divide-outline-variant overflow-auto">
            {data.top_signals.map((signal) => (
              <li key={signal.headline} className="py-1.5 text-on-surface">
                {signal.headline}
              </li>
            ))}
          </ul>
          <p className="shrink-0 text-[10px] text-outline">
            Signal concept inspired by{" "}
            <a
              href="https://github.com/koala73/worldmonitor"
              target="_blank"
              rel="noopener noreferrer"
              className="underline"
            >
              World Monitor
            </a>{" "}
            by Elie Habib (AGPL-3.0) — independent reimplementation, no
            shared code.
          </p>
        </div>
      )}
    </Panel>
  );
}
