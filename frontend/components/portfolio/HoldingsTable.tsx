import type { Holding } from "@/lib/types";
import { Panel } from "@/components/ui/Panel";
import { PriceChange } from "@/components/ui/PriceChange";

export function HoldingsTable({ holdings }: { holdings: Holding[] }) {
  return (
    <Panel title="Holdings" className="h-full">
      <table className="w-full text-[11px]">
        <thead className="sticky top-0 bg-surface-container-lowest text-on-surface-dim">
          <tr>
            <th className="px-3 py-1.5 text-left font-medium">Symbol</th>
            <th className="px-3 py-1.5 text-right font-medium">Qty</th>
            <th className="px-3 py-1.5 text-right font-medium">Avg Cost</th>
            <th className="px-3 py-1.5 text-right font-medium">Price</th>
            <th className="px-3 py-1.5 text-right font-medium">Value</th>
            <th className="px-3 py-1.5 text-right font-medium">PnL</th>
            <th className="px-3 py-1.5 text-center font-medium">Halal</th>
          </tr>
        </thead>
        <tbody>
          {holdings.map((h) => (
            <tr
              key={h.id}
              className="border-t border-outline-variant hover:bg-surface-container"
            >
              <td className="px-3 py-1.5 font-semibold text-on-surface">
                {h.symbol}
              </td>
              <td className="px-3 py-1.5 text-right tabular text-on-surface-dim">
                {h.quantity}
              </td>
              <td className="px-3 py-1.5 text-right tabular text-on-surface-dim">
                {h.average_cost.toFixed(2)}
              </td>
              <td className="px-3 py-1.5 text-right tabular text-on-surface">
                {h.current_price.toFixed(2)}
              </td>
              <td className="px-3 py-1.5 text-right tabular text-on-surface">
                {h.market_value.toLocaleString(undefined, {
                  maximumFractionDigits: 2,
                })}
              </td>
              <td className="px-3 py-1.5 text-right">
                <PriceChange
                  change={h.unrealized_pnl}
                  changePercent={h.unrealized_pnl_percent}
                  compact
                />
              </td>
              <td className="px-3 py-1.5 text-center">
                <span
                  className={
                    h.is_shariah_compliant ? "text-trade-up" : "text-trade-down"
                  }
                >
                  {h.is_shariah_compliant ? "✓" : "✕"}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </Panel>
  );
}
