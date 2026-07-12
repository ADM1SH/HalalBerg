"use client";

import { api } from "@/lib/api";
import { usePolling } from "@/lib/usePolling";
import type { GoldSilverSpot, NisabThreshold } from "@/lib/types";
import { Panel } from "@/components/ui/Panel";

export function GoldNisabPanel() {
  const spot = usePolling<GoldSilverSpot[]>(
    (signal) => api.goldSilverSpot(signal) as Promise<GoldSilverSpot[]>,
    10000
  );
  const nisab = usePolling<NisabThreshold>(
    (signal) => api.nisab(signal) as Promise<NisabThreshold>,
    30000
  );

  const gold = spot.data?.find((s) => s.metal === "gold");
  const silver = spot.data?.find((s) => s.metal === "silver");

  return (
    <Panel title="Gold / Silver & Nisab" className="h-full">
      <div className="grid grid-cols-2 gap-3 p-3 text-[11px]">
        <MetalCell label="Gold / oz" spot={gold} />
        <MetalCell label="Silver / oz" spot={silver} />
      </div>
      {nisab.data && (
        <div className="border-t border-outline-variant px-3 py-2 text-[11px]">
          <p className="text-on-surface-dim">
            Applicable Nisab (silver standard)
          </p>
          <p className="tabular text-lg font-semibold text-secondary">
            ${nisab.data.applicable_nisab_value.toLocaleString()}
          </p>
        </div>
      )}
      {(spot.error || nisab.error) && (
        <p className="p-3 text-[11px] text-trade-down">
          {spot.error ?? nisab.error}
        </p>
      )}
    </Panel>
  );
}

function MetalCell({
  label,
  spot,
}: {
  label: string;
  spot?: GoldSilverSpot;
}) {
  return (
    <div className="rounded-sm border border-outline-variant bg-surface-container p-2">
      <p className="text-on-surface-dim">{label}</p>
      <p className="tabular text-base font-semibold text-on-surface">
        {spot ? `$${spot.spot_price_per_ounce.toFixed(2)}` : "—"}
      </p>
      {spot && (
        <p
          className={`tabular ${
            spot.change_percent >= 0 ? "text-trade-up" : "text-trade-down"
          }`}
        >
          {spot.change_percent >= 0 ? "+" : ""}
          {spot.change_percent.toFixed(2)}%
        </p>
      )}
    </div>
  );
}
