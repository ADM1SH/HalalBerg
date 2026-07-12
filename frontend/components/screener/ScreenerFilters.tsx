"use client";

export interface ScreenerFilterState {
  search: string;
  status: "" | "compliant" | "non_compliant" | "questionable";
  sector: string;
}

export function ScreenerFilters({
  value,
  onChange,
  sectors,
}: {
  value: ScreenerFilterState;
  onChange: (next: ScreenerFilterState) => void;
  sectors: string[];
}) {
  return (
    <div className="flex flex-wrap items-center gap-2 border-b border-outline-variant bg-surface-container-lowest p-2">
      <input
        type="text"
        placeholder="Search symbol or name..."
        value={value.search}
        onChange={(e) => onChange({ ...value, search: e.target.value })}
        className="w-56 rounded-sm border border-outline bg-surface px-2 py-1 text-xs text-on-surface placeholder:text-on-surface-dim focus:border-primary focus:outline-none"
      />
      <select
        value={value.status}
        onChange={(e) =>
          onChange({ ...value, status: e.target.value as ScreenerFilterState["status"] })
        }
        className="rounded-sm border border-outline bg-surface px-2 py-1 text-xs text-on-surface focus:border-primary focus:outline-none"
      >
        <option value="">All compliance</option>
        <option value="compliant">Compliant</option>
        <option value="questionable">Questionable</option>
        <option value="non_compliant">Non-compliant</option>
      </select>
      <select
        value={value.sector}
        onChange={(e) => onChange({ ...value, sector: e.target.value })}
        className="rounded-sm border border-outline bg-surface px-2 py-1 text-xs text-on-surface focus:border-primary focus:outline-none"
      >
        <option value="">All sectors</option>
        {sectors.map((s) => (
          <option key={s} value={s}>
            {s}
          </option>
        ))}
      </select>
    </div>
  );
}
