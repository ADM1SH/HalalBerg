"use client";

import { api } from "@/lib/api";
import { usePolling } from "@/lib/usePolling";
import type { NewsItem } from "@/lib/types";

export function NewsTicker() {
  const { data } = usePolling<NewsItem[]>(
    (signal) => api.news(signal) as Promise<NewsItem[]>,
    30000
  );

  const headlines = data ?? [];
  if (headlines.length === 0) return null;

  // Duplicated so the CSS marquee loops seamlessly at -50%.
  const track = [...headlines, ...headlines];

  return (
    <div className="flex h-6 shrink-0 items-center overflow-hidden border-b border-outline-variant bg-surface-container-lowest">
      <span className="shrink-0 bg-primary px-2 text-[10px] font-semibold uppercase tracking-wide text-background">
        Live
      </span>
      <div className="animate-ticker flex shrink-0 whitespace-nowrap">
        {track.map((item, i) => (
          <span key={`${item.id}-${i}`} className="px-4 text-[11px] text-on-surface-dim">
            {item.source} · {item.headline}
          </span>
        ))}
      </div>
    </div>
  );
}
