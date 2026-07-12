"use client";

import { api } from "@/lib/api";
import { usePolling } from "@/lib/usePolling";
import type { Quote, ShariahAssessment } from "@/lib/types";
import { Panel } from "@/components/ui/Panel";
import { PriceChange } from "@/components/ui/PriceChange";
import { TradingViewChart } from "@/components/stock/TradingViewChart";

const STATUS_STYLE: Record<ShariahAssessment["status"], string> = {
  compliant: "text-trade-up",
  questionable: "text-secondary",
  non_compliant: "text-trade-down",
};

export function StockDetail({ symbol }: { symbol: string }) {
  const quote = usePolling<Quote>(
    (signal) => api.quote(symbol, signal) as Promise<Quote>,
    5000
  );
  const assessment = usePolling<ShariahAssessment>(
    (signal) => api.shariahAssessment(symbol, signal) as Promise<ShariahAssessment>,
    30000
  );

  if (quote.error) {
    return (
      <div className="flex h-full items-center justify-center text-sm text-trade-down">
        {quote.error}
      </div>
    );
  }

  const q = quote.data;
  const a = assessment.data;

  return (
    <div className="grid h-full grid-cols-1 gap-2 p-2 md:grid-cols-3">
      <Panel title={q ? `${q.symbol} — ${q.name}` : symbol} className="h-56 md:col-span-2">
        {q && (
          <div className="p-4">
            <p className="tabular text-3xl font-semibold text-on-surface">
              {q.price.toFixed(2)}
            </p>
            <PriceChange change={q.change} changePercent={q.change_percent} />
            <div className="mt-4 grid grid-cols-3 gap-3 text-[11px]">
              <Stat label="Sector" value={q.sector} />
              <Stat label="Volume" value={q.volume.toLocaleString()} />
              <Stat
                label="Market Cap"
                value={`$${(q.market_cap / 1_000_000_000).toFixed(1)}B`}
              />
            </div>
          </div>
        )}
      </Panel>

      <Panel title="Shariah Assessment" className="h-56">
        {a ? (
          <div className="p-4 text-[11px]">
            <p className={`text-base font-semibold ${STATUS_STYLE[a.status]}`}>
              {a.status.replace("_", " ").toUpperCase()}
            </p>
            <div className="mt-3 space-y-2">
              <Stat
                label="Debt / Market Cap"
                value={`${(a.debt_to_market_cap * 100).toFixed(1)}%`}
              />
              <Stat
                label="Interest Income Ratio"
                value={`${(a.interest_income_ratio * 100).toFixed(1)}%`}
              />
              <Stat
                label="Non-compliant Income"
                value={`${(a.non_compliant_income_ratio * 100).toFixed(1)}%`}
              />
            </div>
            {a.notes && (
              <p className="mt-3 text-on-surface-dim">{a.notes}</p>
            )}
          </div>
        ) : (
          <p className="p-4 text-on-surface-dim">Loading assessment...</p>
        )}
      </Panel>

      <Panel title={`${symbol} — Chart`} className="h-[600px] md:col-span-3">
        <TradingViewChart symbol={symbol} />
      </Panel>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-on-surface-dim">{label}</p>
      <p className="tabular font-medium text-on-surface">{value}</p>
    </div>
  );
}
