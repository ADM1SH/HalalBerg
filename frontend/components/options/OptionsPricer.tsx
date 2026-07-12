"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import type { BlackScholesRequest, BlackScholesResult } from "@/lib/types";
import { Panel } from "@/components/ui/Panel";

const DEFAULTS: BlackScholesRequest = {
  spot_price: 100,
  strike_price: 100,
  time_to_expiry_years: 0.5,
  risk_free_rate: 0.045,
  volatility: 0.25,
  option_type: "call",
};

export function OptionsPricer() {
  const [form, setForm] = useState<BlackScholesRequest>(DEFAULTS);
  const [result, setResult] = useState<BlackScholesResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const update = (field: keyof BlackScholesRequest, value: number | string) =>
    setForm((f) => ({ ...f, [field]: value }));

  const price = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.blackScholes<BlackScholesRequest, BlackScholesResult>(
        form
      );
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Pricing failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid h-full grid-cols-1 gap-2 p-2 md:grid-cols-2">
      <Panel title="Black-Scholes Inputs (FinancePy)">
        <div className="grid grid-cols-2 gap-3 p-3 text-[11px]">
          <Field
            label="Spot Price"
            value={form.spot_price}
            onChange={(v) => update("spot_price", v)}
          />
          <Field
            label="Strike Price"
            value={form.strike_price}
            onChange={(v) => update("strike_price", v)}
          />
          <Field
            label="Time to Expiry (yrs)"
            value={form.time_to_expiry_years}
            step={0.05}
            onChange={(v) => update("time_to_expiry_years", v)}
          />
          <Field
            label="Risk-free Rate"
            value={form.risk_free_rate}
            step={0.005}
            onChange={(v) => update("risk_free_rate", v)}
          />
          <Field
            label="Volatility"
            value={form.volatility}
            step={0.01}
            onChange={(v) => update("volatility", v)}
          />
          <div>
            <label className="mb-1 block text-on-surface-dim">Option Type</label>
            <select
              value={form.option_type}
              onChange={(e) => update("option_type", e.target.value)}
              className="w-full rounded-sm border border-outline bg-surface px-2 py-1 text-on-surface focus:border-primary focus:outline-none"
            >
              <option value="call">Call</option>
              <option value="put">Put</option>
            </select>
          </div>
        </div>
        <div className="p-3">
          <button
            onClick={price}
            disabled={loading}
            className="rounded-sm bg-primary px-4 py-1.5 text-xs font-semibold text-background hover:bg-primary-dim disabled:opacity-50"
          >
            {loading ? "Pricing..." : "Price Option"}
          </button>
        </div>
      </Panel>

      <Panel title="Pricing Result">
        {error && <p className="p-3 text-[11px] text-trade-down">{error}</p>}
        {!error && !result && (
          <p className="p-3 text-[11px] text-on-surface-dim">
            Enter parameters and click Price Option.
          </p>
        )}
        {result && (
          <div className="grid grid-cols-2 gap-3 p-3 text-[11px]">
            <ResultCell label="Price" value={result.price.toFixed(4)} highlight />
            <ResultCell label="Delta" value={result.delta.toFixed(4)} />
            <ResultCell label="Gamma" value={result.gamma.toFixed(4)} />
            <ResultCell label="Vega" value={result.vega.toFixed(4)} />
            <ResultCell label="Theta" value={result.theta.toFixed(4)} />
            <ResultCell label="Rho" value={result.rho.toFixed(4)} />
          </div>
        )}
      </Panel>
    </div>
  );
}

function Field({
  label,
  value,
  onChange,
  step = 1,
}: {
  label: string;
  value: number;
  onChange: (value: number) => void;
  step?: number;
}) {
  return (
    <div>
      <label className="mb-1 block text-on-surface-dim">{label}</label>
      <input
        type="number"
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="tabular w-full rounded-sm border border-outline bg-surface px-2 py-1 text-on-surface focus:border-primary focus:outline-none"
      />
    </div>
  );
}

function ResultCell({
  label,
  value,
  highlight = false,
}: {
  label: string;
  value: string;
  highlight?: boolean;
}) {
  return (
    <div className="rounded-sm border border-outline-variant bg-surface-container p-2">
      <p className="text-on-surface-dim">{label}</p>
      <p
        className={`tabular text-base font-semibold ${
          highlight ? "text-secondary" : "text-on-surface"
        }`}
      >
        {value}
      </p>
    </div>
  );
}
