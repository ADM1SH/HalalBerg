import { StockDetail } from "@/components/stock/StockDetail";

export default async function StockDetailPage({
  params,
}: {
  params: Promise<{ symbol: string }>;
}) {
  const { symbol } = await params;
  return (
    <div className="h-full">
      <StockDetail symbol={symbol.toUpperCase()} />
    </div>
  );
}
