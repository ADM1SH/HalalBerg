import Link from "next/link";
import type { ScreenerRow } from "@/lib/types";

const STATUS_STYLE: Record<ScreenerRow["status"], string> = {
  compliant: "text-trade-up",
  questionable: "text-secondary",
  non_compliant: "text-trade-down",
};

const STATUS_LABEL: Record<ScreenerRow["status"], string> = {
  compliant: "Compliant",
  questionable: "Questionable",
  non_compliant: "Non-compliant",
};

export function ScreenerTable({ rows }: { rows: ScreenerRow[] }) {
  return (
    <table className="w-full text-[11px]">
      <thead className="sticky top-0 bg-surface-container-lowest text-on-surface-dim">
        <tr>
          <th className="px-3 py-1.5 text-left font-medium">Symbol</th>
          <th className="px-3 py-1.5 text-left font-medium">Name</th>
          <th className="px-3 py-1.5 text-left font-medium">Sector</th>
          <th className="px-3 py-1.5 text-right font-medium">Price</th>
          <th className="px-3 py-1.5 text-right font-medium">Mkt Cap</th>
          <th className="px-3 py-1.5 text-right font-medium">Debt/Cap</th>
          <th className="px-3 py-1.5 text-right font-medium">Non-Compl Inc</th>
          <th className="px-3 py-1.5 text-left font-medium">Status</th>
          <th className="px-3 py-1.5 text-left font-medium">Why</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((r) => (
          <tr
            key={r.symbol}
            className="border-t border-outline-variant hover:bg-surface-container"
          >
            <td className="px-3 py-1.5">
              <Link
                href={`/stock/${r.symbol}`}
                className="font-semibold text-on-surface hover:text-primary"
              >
                {r.symbol}
              </Link>
            </td>
            <td className="px-3 py-1.5 text-on-surface-dim">{r.name}</td>
            <td className="px-3 py-1.5 text-on-surface-dim">{r.sector}</td>
            <td className="px-3 py-1.5 text-right tabular text-on-surface">
              {r.price.toFixed(2)}
            </td>
            <td className="px-3 py-1.5 text-right tabular text-on-surface-dim">
              ${(r.market_cap / 1_000_000_000).toFixed(1)}B
            </td>
            <td className="px-3 py-1.5 text-right tabular text-on-surface-dim">
              {(r.debt_to_market_cap * 100).toFixed(1)}%
            </td>
            <td className="px-3 py-1.5 text-right tabular text-on-surface-dim">
              {(r.non_compliant_income_ratio * 100).toFixed(1)}%
            </td>
            <td className={`px-3 py-1.5 font-medium ${STATUS_STYLE[r.status]}`}>
              {STATUS_LABEL[r.status]}
            </td>
            <td title={r.notes} className="px-3 py-1.5 text-on-surface-dim">
              <div className="max-w-48 truncate">{r.notes}</div>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
