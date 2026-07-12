import { TickerTape } from "@/components/dashboard/TickerTape";
import { DashboardBento } from "@/components/dashboard/DashboardBento";

export default function DashboardPage() {
  return (
    <div className="flex h-full flex-col">
      <TickerTape />
      <div className="min-h-0 flex-1">
        <DashboardBento />
      </div>
    </div>
  );
}
