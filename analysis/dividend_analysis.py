import pandas as pd
from typing import Dict, Optional
from models.schemas import DividendMetrics
from config.config import MIN_DY_THRESHOLD

_MIN_YEARS_FOR_STABILITY = 2
_CONSISTENT_YEARS_RATIO = 0.8  # pagou em >= 80% dos anos observados
_MIN_PRICE_POINTS_FOR_VOLATILITY = 20
_LOW_VOLATILITY_THRESHOLD = 0.20
_HIGH_VOLATILITY_THRESHOLD = 0.40


def _compute_stability_note(dividend_history: Optional[pd.Series]) -> str:
    """
    Deriva a consistência de pagamento a partir do histórico real de proventos
    (yfinance `Ticker.dividends`). Sem histórico suficiente, cai no placeholder
    genérico "Regular" (comportamento anterior, preservado como fallback).
    """
    if dividend_history is None or dividend_history.empty:
        return "Regular"

    years_with_payment = {timestamp.year for timestamp in dividend_history.index}
    if len(years_with_payment) < _MIN_YEARS_FOR_STABILITY:
        return "Histórico insuficiente"

    span_years = max(years_with_payment) - min(years_with_payment) + 1
    payment_ratio = len(years_with_payment) / span_years

    return "Consistente" if payment_ratio >= _CONSISTENT_YEARS_RATIO else "Irregular"


def _compute_volatility_flag(price_df: pd.DataFrame) -> str:
    """
    Deriva a flag de volatilidade a partir da volatilidade anualizada real do
    preço. Sem histórico suficiente, cai no placeholder "medium" (comportamento
    anterior, preservado como fallback).
    """
    if price_df is None or price_df.empty or len(price_df) < _MIN_PRICE_POINTS_FOR_VOLATILITY:
        return "medium"

    returns = price_df["Close"].pct_change().dropna().tail(60)
    if returns.empty:
        return "medium"

    annualized_volatility = returns.std() * (252 ** 0.5)
    if pd.isna(annualized_volatility):
        return "medium"

    if annualized_volatility < _LOW_VOLATILITY_THRESHOLD:
        return "low"
    if annualized_volatility > _HIGH_VOLATILITY_THRESHOLD:
        return "high"
    return "medium"


def analyze_dividends(
    ticker: str,
    fundamentals: Dict,
    price_df: pd.DataFrame,
    dividend_history: Optional[pd.Series] = None,
) -> DividendMetrics:
    """
    Analisa métricas de dividendos: yield, score de 0 a 1, consistência de
    pagamento (real, se `dividend_history` for informado) e flag de
    volatilidade (real, a partir de `price_df`).
    """
    dy = fundamentals.get("dividend_yield", 0.0)

    score = 0.0
    summary = "Sem dados de dividendos relevantes."
    stability = "Indefinida"

    if dy > 0:
        # Normalização simples: 6% = 0.5, 12% = 1.0
        score = min(dy / (MIN_DY_THRESHOLD * 2), 1.0)

        if dy < MIN_DY_THRESHOLD:
            summary = f"DY de {dy:.2%} abaixo do limiar de {MIN_DY_THRESHOLD:.0%}."
        else:
            summary = f"Bom pagador de dividendos: {dy:.2%}."

        stability = _compute_stability_note(dividend_history)

    vol_flag = _compute_volatility_flag(price_df)

    return DividendMetrics(
        dy=dy,
        dividend_score=score,
        stability_note=stability,
        volatility_flag=vol_flag,
        summary_pt=summary
    )
