export function PriceChange({
  change,
  changePercent,
  compact = false,
}: {
  change: number;
  changePercent: number;
  compact?: boolean;
}) {
  const isUp = change > 0;
  const isFlat = change === 0;
  const color = isFlat
    ? "text-trade-neutral"
    : isUp
      ? "text-trade-up"
      : "text-trade-down";
  const sign = isUp ? "+" : "";

  return (
    <span className={`tabular ${color}`}>
      {sign}
      {change.toFixed(2)}
      {!compact && (
        <>
          {" "}
          ({sign}
          {changePercent.toFixed(2)}%)
        </>
      )}
    </span>
  );
}
