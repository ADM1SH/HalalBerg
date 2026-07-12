"use client";

import { api } from "@/lib/api";
import { usePolling } from "@/lib/usePolling";
import type { NewsItem } from "@/lib/types";
import { Panel } from "@/components/ui/Panel";

const SENTIMENT_COLOR: Record<NewsItem["sentiment"], string> = {
  positive: "text-trade-up",
  neutral: "text-trade-neutral",
  negative: "text-trade-down",
};

export function NewsPanel() {
  const { data, error } = usePolling<NewsItem[]>(
    (signal) => api.news(signal) as Promise<NewsItem[]>,
    15000
  );

  return (
    <Panel title="News Feed" className="h-full">
      {error && <p className="p-3 text-[11px] text-trade-down">{error}</p>}
      <ul className="divide-y divide-outline-variant">
        {(data ?? []).map((item) => (
          <li key={item.id} className="p-3 text-[11px]">
            <div className="flex items-start justify-between gap-2">
              <p className="text-on-surface">{item.headline}</p>
              <span
                className={`shrink-0 text-[10px] uppercase ${SENTIMENT_COLOR[item.sentiment]}`}
              >
                {item.sentiment}
              </span>
            </div>
            <p className="mt-1 text-on-surface-dim">
              {item.source} · {new Date(item.published_at).toLocaleTimeString()}
            </p>
            {item.related_symbols.length > 0 && (
              <p className="mt-1 tabular text-primary">
                {item.related_symbols.join(", ")}
              </p>
            )}
          </li>
        ))}
      </ul>
    </Panel>
  );
}
