"use client";

import { api } from "@/lib/api";
import { usePolling } from "@/lib/usePolling";
import type { Quote } from "@/lib/types";
import { Panel } from "@/components/ui/Panel";

export function ShariahBreakdownPanel() {
  const { data } = usePolling<Quote[]>(
    (signal) => api.quotes(signal) as Promise<Quote[]>,
    10000
  );

  const quotes = data ?? [];
  const compliant = quotes.filter((q) => q.is_shariah_compliant).length;
  const total = quotes.length;
  const compliantPct = total > 0 ? (compliant / total) * 100 : 0;

  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - compliantPct / 100);

  return (
    <Panel title="Shariah Compliance" className="h-full">
      <div className="flex h-full items-center justify-center gap-4 p-3">
        <svg width="100" height="100" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="var(--color-trade-down)"
            strokeWidth="12"
          />
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="var(--color-trade-up)"
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            transform="rotate(-90 50 50)"
            strokeLinecap="round"
          />
          <text
            x="50"
            y="54"
            textAnchor="middle"
            className="tabular"
            fill="var(--color-on-surface)"
            fontSize="18"
            fontWeight="600"
          >
            {compliantPct.toFixed(0)}%
          </text>
        </svg>
        <div className="text-[11px]">
          <p className="text-trade-up">● Compliant ({compliant})</p>
          <p className="text-trade-down">● Non-compliant ({total - compliant})</p>
          <p className="mt-1 text-on-surface-dim">{total} tracked</p>
        </div>
      </div>
    </Panel>
  );
}
