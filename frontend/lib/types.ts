export interface Quote {
  symbol: string;
  name: string;
  sector: string;
  price: number;
  change: number;
  change_percent: number;
  volume: number;
  market_cap: number;
  is_shariah_compliant: boolean;
}

export interface ShariahAssessment {
  symbol: string;
  status: "compliant" | "non_compliant" | "questionable";
  debt_to_market_cap: number;
  interest_income_ratio: number;
  non_compliant_income_ratio: number;
  notes: string;
}

export interface GoldSilverSpot {
  metal: "gold" | "silver";
  spot_price_per_ounce: number;
  spot_price_per_gram: number;
  change_percent: number;
  as_of: string;
}

export interface NisabThreshold {
  gold_nisab_grams: number;
  silver_nisab_grams: number;
  gold_nisab_value: number;
  silver_nisab_value: number;
  applicable_nisab_value: number;
  as_of: string;
}

export interface NewsItem {
  id: number;
  headline: string;
  summary: string;
  source: string;
  url: string;
  published_at: string;
  related_symbols: string[];
  sentiment: "positive" | "neutral" | "negative";
}

export interface Holding {
  id: number;
  symbol: string;
  name: string;
  quantity: number;
  average_cost: number;
  current_price: number;
  market_value: number;
  unrealized_pnl: number;
  unrealized_pnl_percent: number;
  is_shariah_compliant: boolean;
}

export interface PortfolioSummary {
  total_market_value: number;
  total_cost_basis: number;
  total_unrealized_pnl: number;
  total_unrealized_pnl_percent: number;
  cash_balance: number;
  zakat_due: number;
  zakat_assessment_date: string;
  holdings: Holding[];
}

export interface EfficientFrontierPoint {
  risk: number;
  expected_return: number;
  weights: Record<string, number>;
}

export interface OptimizationResult {
  frontier: EfficientFrontierPoint[];
  max_sharpe: EfficientFrontierPoint;
  min_variance: EfficientFrontierPoint;
}

export interface BlackScholesRequest {
  spot_price: number;
  strike_price: number;
  time_to_expiry_years: number;
  risk_free_rate: number;
  volatility: number;
  option_type: "call" | "put";
}

export interface BlackScholesResult {
  price: number;
  delta: number;
  gamma: number;
  vega: number;
  theta: number;
  rho: number;
}

export interface OptimizationRequest {
  symbols: string[];
}

export interface RiskSignal {
  escalation_score: number;
  level: "low" | "elevated" | "high" | "critical";
  categories: Record<string, number>;
  top_signals: {
    headline: string;
    source: string;
    url: string;
    published_at: string;
    categories: string[];
  }[];
  as_of: string;
}

export interface ScreenerRow {
  symbol: string;
  name: string;
  sector: string;
  price: number;
  market_cap: number;
  status: "compliant" | "non_compliant" | "questionable";
  debt_to_market_cap: number;
  non_compliant_income_ratio: number;
  notes: string;
}
