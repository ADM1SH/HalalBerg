"use client";

import { api } from "@/lib/api";
import { usePolling } from "@/lib/usePolling";
import type { Quote } from "@/lib/types";
import { PriceChange } from "@/components/ui/PriceChange";

export function TickerTape() {
  const { data, error } = usePolling<Quote[]>(
    (signal) => api.quotes(signal) as Promise<Quote[]>,
    4000
  );

  if (error) {
    return (
      <div className="flex h-8 shrink-0 items-center border-b border-outline-variant bg-surface-container-lowest px-3 text-[11px] text-trade-down">
        Market data unavailable — {error}
      </div>
    );
  }

  const quotes = data ?? [];

  return (
    <div className="flex h-8 shrink-0 items-center gap-6 overflow-x-auto border-b border-outline-variant bg-surface-container-lowest px-3 text-[11px] tabular">
      {quotes.length === 0 && (
        <span className="text-on-surface-dim">Loading ticker...</span>
      )}
      {quotes.map((q) => (
        <div key={q.symbol} className="flex shrink-0 items-center gap-1.5">
          <span className="font-semibold text-on-surface">{q.symbol}</span>
          <span className="text-on-surface-dim">{q.price.toFixed(2)}</span>
          <PriceChange change={q.change} changePercent={q.change_percent} compact />
        </div>
      ))}
    </div>
  );
}
