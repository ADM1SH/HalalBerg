"use client";

import { useEffect, useRef } from "react";

// TradingView's real hosted widget — full charting engine (candlesticks,
// 100+ indicators, drawing tools, every timeframe) embedded via their
// official free script, not a reimplementation.
const EXCHANGE_BY_SYMBOL: Record<string, string> = {
  AAPL: "NASDAQ",
  MSFT: "NASDAQ",
  NVDA: "NASDAQ",
  GOOGL: "NASDAQ",
  AMZN: "NASDAQ",
  TSLA: "NASDAQ",
  JNJ: "NYSE",
  JPM: "NYSE",
  BAC: "NYSE",
  XOM: "NYSE",
  KO: "NYSE",
  DIS: "NYSE",
  PFE: "NYSE",
  V: "NYSE",
  PG: "NYSE",
  META: "NASDAQ",
  NFLX: "NASDAQ",
  INTC: "NASDAQ",
  CMCSA: "NASDAQ",
  WMT: "NYSE",
  HD: "NYSE",
  NKE: "NYSE",
  CAT: "NYSE",
  MS: "NYSE",
  T: "NYSE",
};

export function TradingViewChart({ symbol }: { symbol: string }) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    container.innerHTML = "";

    const exchange = EXCHANGE_BY_SYMBOL[symbol] ?? "NASDAQ";
    const script = document.createElement("script");
    script.src =
      "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
    script.type = "text/javascript";
    script.async = true;
    script.text = JSON.stringify({
      autosize: true,
      symbol: `${exchange}:${symbol}`,
      interval: "D",
      timezone: "Etc/UTC",
      theme: "dark",
      style: "1",
      locale: "en",
      hide_top_toolbar: false,
      hide_legend: false,
      allow_symbol_change: false,
      support_host: "https://www.tradingview.com",
    });
    container.appendChild(script);
  }, [symbol]);

  return <div className="tradingview-widget-container h-full w-full" ref={containerRef} />;
}
