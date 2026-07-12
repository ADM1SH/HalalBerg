import { WatchlistPanel } from "./WatchlistPanel";
import { GoldNisabPanel } from "./GoldNisabPanel";
import { NewsPanel } from "./NewsPanel";
import { ShariahBreakdownPanel } from "./ShariahBreakdownPanel";
import { RiskSignalPanel } from "./RiskSignalPanel";
import { LiveChannelsPanel } from "./LiveChannelsPanel";

export function DashboardBento() {
  return (
    <div className="grid h-full grid-cols-1 gap-2 p-2 md:grid-cols-3 md:grid-rows-2">
      <div className="md:col-span-2 md:row-span-2">
        <WatchlistPanel />
      </div>
      <div>
        <GoldNisabPanel />
      </div>
      <div>
        <ShariahBreakdownPanel />
      </div>
      <div className="md:col-span-2">
        <NewsPanel />
      </div>
      <div>
        <RiskSignalPanel />
      </div>
      <div className="md:col-span-3">
        <LiveChannelsPanel />
      </div>
    </div>
  );
}
