import type { PortfolioSummary } from "@/lib/types";

export function SummaryCards({ summary }: { summary: PortfolioSummary }) {
  const cards = [
    {
      label: "Market Value",
      value: `$${summary.total_market_value.toLocaleString(undefined, {
        maximumFractionDigits: 2,
      })}`,
      accent: "text-on-surface",
    },
    {
      label: "Unrealized PnL",
      value: `${summary.total_unrealized_pnl >= 0 ? "+" : ""}$${summary.total_unrealized_pnl.toLocaleString(
        undefined,
        { maximumFractionDigits: 2 }
      )} (${summary.total_unrealized_pnl_percent.toFixed(2)}%)`,
      accent:
        summary.total_unrealized_pnl >= 0 ? "text-trade-up" : "text-trade-down",
    },
    {
      label: "Cash Balance",
      value: `$${summary.cash_balance.toLocaleString(undefined, {
        maximumFractionDigits: 2,
      })}`,
      accent: "text-on-surface",
    },
    {
      label: "Zakat Due",
      value: `$${summary.zakat_due.toLocaleString(undefined, {
        maximumFractionDigits: 2,
      })}`,
      accent: "text-secondary",
    },
  ];

  return (
    <div className="grid grid-cols-2 gap-2 p-2 md:grid-cols-4">
      {cards.map((c) => (
        <div
          key={c.label}
          className="rounded-sm border border-outline-variant bg-surface p-3"
        >
          <p className="text-[11px] uppercase tracking-wide text-on-surface-dim">
            {c.label}
          </p>
          <p className={`tabular mt-1 text-lg font-semibold ${c.accent}`}>
            {c.value}
          </p>
        </div>
      ))}
    </div>
  );
}
