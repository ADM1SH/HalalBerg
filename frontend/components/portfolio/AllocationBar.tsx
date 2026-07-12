import type { Holding } from "@/lib/types";
import { Panel } from "@/components/ui/Panel";

const PALETTE = [
  "#22d3ee",
  "#f5a623",
  "#22c55e",
  "#a855f7",
  "#ef4444",
  "#eab308",
  "#38bdf8",
  "#f472b6",
];

export function AllocationBar({ holdings }: { holdings: Holding[] }) {
  const total = holdings.reduce((sum, h) => sum + h.market_value, 0);
  const sorted = [...holdings].sort((a, b) => b.market_value - a.market_value);

  return (
    <Panel title="Allocation" className="h-full" bodyClassName="p-3">
      <div className="flex h-3 w-full overflow-hidden rounded-sm">
        {sorted.map((h, i) => (
          <div
            key={h.id}
            style={{
              width: `${total > 0 ? (h.market_value / total) * 100 : 0}%`,
              backgroundColor: PALETTE[i % PALETTE.length],
            }}
            title={`${h.symbol}: ${((h.market_value / total) * 100).toFixed(1)}%`}
          />
        ))}
      </div>
      <ul className="mt-3 space-y-1 text-[11px]">
        {sorted.map((h, i) => (
          <li key={h.id} className="flex items-center justify-between">
            <span className="flex items-center gap-2">
              <span
                className="inline-block h-2 w-2 rounded-full"
                style={{ backgroundColor: PALETTE[i % PALETTE.length] }}
              />
              <span className="text-on-surface">{h.symbol}</span>
            </span>
            <span className="tabular text-on-surface-dim">
              {total > 0 ? ((h.market_value / total) * 100).toFixed(1) : "0.0"}%
            </span>
          </li>
        ))}
      </ul>
    </Panel>
  );
}
