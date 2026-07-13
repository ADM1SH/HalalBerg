import type { ReactNode } from "react";
import { TopNavBar } from "./TopNavBar";
import { SideNavBar } from "./SideNavBar";
import { NewsTicker } from "./NewsTicker";

export function TerminalShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-screen w-screen flex-col overflow-hidden bg-background">
      <TopNavBar />
      <NewsTicker />
      <div className="flex min-h-0 flex-1">
        <SideNavBar />
        <main className="min-w-0 flex-1 overflow-auto">{children}</main>
      </div>
    </div>
  );
}
