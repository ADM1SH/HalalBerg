"use client";

import Link from "next/link";
import { api } from "@/lib/api";
import { usePolling } from "@/lib/usePolling";
import type { Quote } from "@/lib/types";
import { Panel } from "@/components/ui/Panel";
import { PriceChange } from "@/components/ui/PriceChange";

export function WatchlistPanel() {
  const { data, error } = usePolling<Quote[]>(
    (signal) => api.quotes(signal) as Promise<Quote[]>,
    5000
  );

  return (
    <Panel title="Watchlist" className="h-full">
      {error && (
        <p className="p-3 text-[11px] text-trade-down">{error}</p>
      )}
      <table className="w-full text-[11px]">
        <thead className="sticky top-0 bg-surface-container-lowest text-on-surface-dim">
          <tr>
            <th className="px-3 py-1.5 text-left font-medium">Symbol</th>
            <th className="px-3 py-1.5 text-left font-medium">Sector</th>
            <th className="px-3 py-1.5 text-right font-medium">Price</th>
            <th className="px-3 py-1.5 text-right font-medium">Chg</th>
            <th className="px-3 py-1.5 text-center font-medium">Halal</th>
          </tr>
        </thead>
        <tbody>
          {(data ?? []).map((q) => (
            <tr
              key={q.symbol}
              className="border-t border-outline-variant hover:bg-surface-container"
            >
              <td className="px-3 py-1.5">
                <Link
                  href={`/stock/${q.symbol}`}
                  className="font-semibold text-on-surface hover:text-primary"
                >
                  {q.symbol}
                </Link>
              </td>
              <td className="px-3 py-1.5 text-on-surface-dim">{q.sector}</td>
              <td className="px-3 py-1.5 text-right tabular text-on-surface">
                {q.price.toFixed(2)}
              </td>
              <td className="px-3 py-1.5 text-right">
                <PriceChange change={q.change} changePercent={q.change_percent} compact />
              </td>
              <td className="px-3 py-1.5 text-center">
                <span
                  className={
                    q.is_shariah_compliant ? "text-trade-up" : "text-trade-down"
                  }
                >
                  {q.is_shariah_compliant ? "✓" : "✕"}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </Panel>
  );
}
