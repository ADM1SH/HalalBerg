"""
Quant compute layer bridging the external optimization/pricing libraries
(cvxpy, FinancePy) referenced in the project's external_repos.

Expected returns and covariance come from real trailing-1y daily closes
(apps.market.providers.yahoo_daily_closes), cached per symbol for an hour so
repeated frontier requests don't refetch history every time.
"""

import cvxpy as cp
import numpy as np
from django.core.cache import cache
from financepy.market.curves.discount_curve_flat import DiscountCurveFlat
from financepy.models.black_scholes import BlackScholes
from financepy.products.equity.equity_vanilla_option import EquityVanillaOption
from financepy.utils.date import Date
from financepy.utils.global_types import OptionTypes

from apps.market.providers import yahoo_daily_closes

TRADING_DAYS_PER_YEAR = 252
HISTORY_CACHE_SECONDS = 60 * 60


def _daily_log_returns(symbol: str) -> np.ndarray:
    cache_key = f"quant_returns:{symbol}"
    cached = cache.get(cache_key)
    if cached is not None:
        return np.array(cached)

    closes = np.array(yahoo_daily_closes(symbol, range_="1y")["closes"], dtype=float)
    returns = np.diff(np.log(closes))
    cache.set(cache_key, returns.tolist(), timeout=HISTORY_CACHE_SECONDS)
    return returns


def build_return_and_covariance(symbols: list[str]) -> tuple[np.ndarray, np.ndarray]:
    series = [_daily_log_returns(symbol) for symbol in symbols]
    min_len = min(len(r) for r in series)
    aligned = np.array([r[-min_len:] for r in series])  # (n_symbols, n_days)

    expected_returns = aligned.mean(axis=1) * TRADING_DAYS_PER_YEAR
    covariance = np.atleast_2d(np.cov(aligned)) * TRADING_DAYS_PER_YEAR
    return expected_returns, covariance


def compute_efficient_frontier(symbols: list[str], n_points: int = 25) -> dict:
    expected_returns, covariance = build_return_and_covariance(symbols)
    n = len(symbols)

    min_ret, max_ret = float(expected_returns.min()), float(expected_returns.max())
    targets = np.linspace(min_ret, max_ret, n_points)

    frontier = []
    best_sharpe = -np.inf
    max_sharpe_point = None
    min_variance_point = None
    min_variance_risk = np.inf

    risk_free_rate = 0.045

    for target in targets:
        w = cp.Variable(n)
        risk = cp.quad_form(w, cp.psd_wrap(covariance))
        constraints = [cp.sum(w) == 1, w >= 0, expected_returns @ w >= target]
        problem = cp.Problem(cp.Minimize(risk), constraints)
        problem.solve(solver=cp.CLARABEL)

        if w.value is None:
            continue

        weights = np.clip(w.value, 0, None)
        weights = weights / weights.sum()
        point_risk = float(np.sqrt(weights @ covariance @ weights))
        point_return = float(expected_returns @ weights)

        point = {
            "risk": round(point_risk, 4),
            "expected_return": round(point_return, 4),
            "weights": {
                symbol: round(float(weight), 4)
                for symbol, weight in zip(symbols, weights)
            },
        }
        frontier.append(point)

        sharpe = (point_return - risk_free_rate) / point_risk if point_risk > 0 else -np.inf
        if sharpe > best_sharpe:
            best_sharpe = sharpe
            max_sharpe_point = point
        if point_risk < min_variance_risk:
            min_variance_risk = point_risk
            min_variance_point = point

    return {
        "frontier": frontier,
        "max_sharpe": max_sharpe_point,
        "min_variance": min_variance_point,
    }


def price_black_scholes(
    spot_price: float,
    strike_price: float,
    time_to_expiry_years: float,
    risk_free_rate: float,
    volatility: float,
    option_type: str,
) -> dict:
    value_dt = Date(1, 1, 2026)
    expiry_dt = value_dt.add_years(time_to_expiry_years)
    opt_type = (
        OptionTypes.EUROPEAN_CALL if option_type == "call" else OptionTypes.EUROPEAN_PUT
    )

    option = EquityVanillaOption(expiry_dt, strike_price, opt_type)
    discount_curve = DiscountCurveFlat(value_dt, risk_free_rate)
    dividend_curve = DiscountCurveFlat(value_dt, 0.0)
    model = BlackScholes(volatility)

    args = (value_dt, spot_price, discount_curve, dividend_curve, model)

    return {
        "price": round(float(option.value(*args)), 4),
        "delta": round(float(option.delta(*args)), 4),
        "gamma": round(float(option.gamma(*args)), 4),
        "vega": round(float(option.vega(*args)), 4),
        "theta": round(float(option.theta(*args)), 4),
        "rho": round(float(option.rho(*args)), 4),
    }
