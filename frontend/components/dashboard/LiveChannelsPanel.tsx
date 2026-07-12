"use client";

import { useState } from "react";
import { Panel } from "@/components/ui/Panel";

// Real, verified YouTube channel IDs — the /embed/live_stream?channel=
// format always resolves to whatever that channel is currently
// broadcasting live, no API key needed.
const CHANNELS = [
  { id: "UCIALMKvObZNtJ6AmdCLP7Lg", label: "Bloomberg TV" },
  { id: "UCNye-wNBqNL5ZzHSJj3l8Bg", label: "Al Jazeera English" },
  { id: "UCEAZeUIeJs0IjQiqTCdVSIg", label: "Yahoo Finance" },
];

export function LiveChannelsPanel() {
  const [channel, setChannel] = useState(CHANNELS[0]);

  return (
    <Panel
      title="Live Channels"
      className="h-full"
      accessory={
        <div className="flex gap-1">
          {CHANNELS.map((c) => (
            <button
              key={c.id}
              onClick={() => setChannel(c)}
              className={`rounded-sm px-2 py-0.5 text-[10px] uppercase tracking-wide ${
                channel.id === c.id
                  ? "bg-primary text-background"
                  : "text-on-surface-dim hover:text-on-surface"
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>
      }
    >
      <div className="flex h-full flex-col">
        <div className="aspect-video w-full bg-black">
          <iframe
            key={channel.id}
            src={`https://www.youtube.com/embed/live_stream?channel=${channel.id}`}
            title={channel.label}
            className="h-full w-full"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        </div>
        <p className="p-2 text-[10px] text-outline">
          Live channel embeds inspired by{" "}
          <a
            href="https://github.com/koala73/worldmonitor"
            target="_blank"
            rel="noopener noreferrer"
            className="underline"
          >
            World Monitor
          </a>{" "}
          by Elie Habib (AGPL-3.0) — independent implementation via
          YouTube&apos;s public live-stream embed, no shared code.
        </p>
      </div>
    </Panel>
  );
}
