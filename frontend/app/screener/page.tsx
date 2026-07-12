"use client";

import { useMemo, useState } from "react";
import { api } from "@/lib/api";
import { usePolling } from "@/lib/usePolling";
import type { ScreenerRow } from "@/lib/types";
import { Panel } from "@/components/ui/Panel";
import {
  ScreenerFilters,
  type ScreenerFilterState,
} from "@/components/screener/ScreenerFilters";
import { ScreenerTable } from "@/components/screener/ScreenerTable";

export default function ScreenerPage() {
  const [filters, setFilters] = useState<ScreenerFilterState>({
    search: "",
    status: "",
    sector: "",
  });

  const queryString = useMemo(() => {
    const params = new URLSearchParams();
    if (filters.search) params.set("search", filters.search);
    if (filters.status) params.set("status", filters.status);
    if (filters.sector) params.set("sector", filters.sector);
    return params.toString();
  }, [filters]);

  const { data, error, loading } = usePolling<ScreenerRow[]>(
    (signal) => api.screener(queryString, signal) as Promise<ScreenerRow[]>,
    10000
  );

  const rows = data ?? [];
  const sectors = useMemo(
    () => Array.from(new Set(rows.map((r) => r.sector))).sort(),
    [rows]
  );

  return (
    <div className="flex h-full flex-col">
      <Panel title="Equity Screener" className="h-full m-2">
        <ScreenerFilters value={filters} onChange={setFilters} sectors={sectors} />
        {loading && (
          <p className="p-3 text-[11px] text-on-surface-dim">Loading screener...</p>
        )}
        {error && <p className="p-3 text-[11px] text-trade-down">{error}</p>}
        {!loading && !error && <ScreenerTable rows={rows} />}
      </Panel>
    </div>
  );
}
