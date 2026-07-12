"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { usePolling } from "@/lib/usePolling";
import type { OptimizationRequest, OptimizationResult, Quote } from "@/lib/types";
import { Panel } from "@/components/ui/Panel";
import { EfficientFrontierChart } from "./EfficientFrontierChart";

export function OptimizationPanel() {
  const { data: quotes } = usePolling<Quote[]>(
    (signal) => api.quotes(signal) as Promise<Quote[]>,
    30000
  );
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [result, setResult] = useState<OptimizationResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const toggle = (symbol: string) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(symbol)) next.delete(symbol);
      else next.add(symbol);
      return next;
    });
  };

  const optimize = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.efficientFrontier<OptimizationRequest, OptimizationResult>({
        symbols: Array.from(selected),
      });
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Optimization failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid h-full grid-cols-1 gap-2 p-2 md:grid-cols-3">
      <Panel title="Universe (cvxpy)">
        <ul className="p-2 text-[11px]">
          {(quotes ?? [])
            .filter((q) => q.is_shariah_compliant)
            .map((q) => (
              <li key={q.symbol} className="flex items-center gap-2 py-1">
                <input
                  type="checkbox"
                  checked={selected.has(q.symbol)}
                  onChange={() => toggle(q.symbol)}
                  className="accent-primary"
                />
                <span className="text-on-surface">{q.symbol}</span>
                <span className="text-on-surface-dim">{q.name}</span>
              </li>
            ))}
        </ul>
        <div className="p-2">
          <button
            onClick={optimize}
            disabled={loading || selected.size < 2}
            className="rounded-sm bg-primary px-4 py-1.5 text-xs font-semibold text-background hover:bg-primary-dim disabled:opacity-50"
          >
            {loading ? "Optimizing..." : "Compute Efficient Frontier"}
          </button>
          {selected.size < 2 && (
            <p className="mt-1 text-[10px] text-on-surface-dim">
              Select at least 2 symbols
            </p>
          )}
        </div>
      </Panel>

      <Panel title="Efficient Frontier" className="md:col-span-2">
        {error && <p className="p-3 text-[11px] text-trade-down">{error}</p>}
        {!error && !result && (
          <p className="p-3 text-[11px] text-on-surface-dim">
            Select holdings and compute the frontier.
          </p>
        )}
        {result && (
          <div className="p-3">
            <EfficientFrontierChart
              frontier={result.frontier}
              maxSharpe={result.max_sharpe}
              minVariance={result.min_variance}
            />
            <div className="mt-2 grid grid-cols-2 gap-3 text-[11px]">
              <WeightsCard title="Max Sharpe" point={result.max_sharpe} color="text-secondary" />
              <WeightsCard title="Min Variance" point={result.min_variance} color="text-trade-up" />
            </div>
          </div>
        )}
      </Panel>
    </div>
  );
}

function WeightsCard({
  title,
  point,
  color,
}: {
  title: string;
  point: OptimizationResult["max_sharpe"];
  color: string;
}) {
  return (
    <div className="rounded-sm border border-outline-variant bg-surface-container p-2">
      <p className={`font-semibold ${color}`}>{title}</p>
      <p className="tabular text-on-surface-dim">
        Risk {point.risk.toFixed(3)} · Return {point.expected_return.toFixed(3)}
      </p>
      <ul className="mt-1 space-y-0.5">
        {Object.entries(point.weights).map(([symbol, weight]) => (
          <li key={symbol} className="tabular flex justify-between text-on-surface">
            <span>{symbol}</span>
            <span>{(weight * 100).toFixed(1)}%</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
