import type { EfficientFrontierPoint } from "@/lib/types";

export function EfficientFrontierChart({
  frontier,
  maxSharpe,
  minVariance,
}: {
  frontier: EfficientFrontierPoint[];
  maxSharpe: EfficientFrontierPoint;
  minVariance: EfficientFrontierPoint;
}) {
  const width = 420;
  const height = 260;
  const padding = 32;

  const risks = frontier.map((p) => p.risk);
  const returns = frontier.map((p) => p.expected_return);
  const minRisk = Math.min(...risks, 0);
  const maxRisk = Math.max(...risks, 0.01);
  const minReturn = Math.min(...returns, 0);
  const maxReturn = Math.max(...returns, 0.01);

  const scaleX = (risk: number) =>
    padding + ((risk - minRisk) / (maxRisk - minRisk || 1)) * (width - padding * 2);
  const scaleY = (ret: number) =>
    height - padding - ((ret - minReturn) / (maxReturn - minReturn || 1)) * (height - padding * 2);

  const points = frontier.map((p) => `${scaleX(p.risk)},${scaleY(p.expected_return)}`);

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="w-full">
      <line
        x1={padding}
        y1={height - padding}
        x2={width - padding}
        y2={height - padding}
        stroke="var(--color-outline)"
      />
      <line
        x1={padding}
        y1={padding}
        x2={padding}
        y2={height - padding}
        stroke="var(--color-outline)"
      />
      <text x={padding} y={height - 8} fontSize="9" fill="var(--color-on-surface-dim)">
        Risk (σ) →
      </text>
      <text
        x={4}
        y={padding}
        fontSize="9"
        fill="var(--color-on-surface-dim)"
        transform={`rotate(-90 12 ${padding})`}
      >
        Return →
      </text>
      <polyline
        points={points.join(" ")}
        fill="none"
        stroke="var(--color-primary)"
        strokeWidth="1.5"
      />
      <circle
        cx={scaleX(minVariance.risk)}
        cy={scaleY(minVariance.expected_return)}
        r="4"
        fill="var(--color-trade-up)"
      />
      <circle
        cx={scaleX(maxSharpe.risk)}
        cy={scaleY(maxSharpe.expected_return)}
        r="4"
        fill="var(--color-secondary)"
      />
    </svg>
  );
}
