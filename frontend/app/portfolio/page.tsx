"use client";

import { api } from "@/lib/api";
import { usePolling } from "@/lib/usePolling";
import type { PortfolioSummary } from "@/lib/types";
import { SummaryCards } from "@/components/portfolio/SummaryCards";
import { HoldingsTable } from "@/components/portfolio/HoldingsTable";
import { AllocationBar } from "@/components/portfolio/AllocationBar";

export default function PortfolioPage() {
  const { data, error, loading } = usePolling<PortfolioSummary>(
    (signal) => api.portfolio(signal) as Promise<PortfolioSummary>,
    8000
  );

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center text-sm text-on-surface-dim">
        Loading portfolio...
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex h-full items-center justify-center text-sm text-trade-down">
        {error ?? "No portfolio data"}
      </div>
    );
  }

  return (
    <div className="flex h-full flex-col">
      <SummaryCards summary={data} />
      <div className="grid min-h-0 flex-1 grid-cols-1 gap-2 p-2 pt-0 md:grid-cols-3">
        <div className="md:col-span-2">
          <HoldingsTable holdings={data.holdings} />
        </div>
        <div>
          <AllocationBar holdings={data.holdings} />
        </div>
      </div>
    </div>
  );
}
