"""SPEC-030: regras de alerta para watchlist."""

from __future__ import annotations

from dataclasses import dataclass

from shared.config.config import MIN_DY_THRESHOLD, RSI_OVERBOUGHT, RSI_OVERSOLD
from shared.models.schemas import AssetAnalysis


@dataclass
class Alert:
    ticker: str
    rule: str
    message: str


def evaluate_alerts(assets: list[AssetAnalysis]) -> list[Alert]:
    alerts: list[Alert] = []
    for a in assets:
        if a.technical and not a.technical.insufficient_history:
            if a.technical.rsi <= RSI_OVERSOLD:
                alerts.append(
                    Alert(
                        a.ticker,
                        "rsi_oversold",
                        f"{a.ticker}: RSI {a.technical.rsi:.1f} ≤ {RSI_OVERSOLD} (oversold)",
                    )
                )
            if a.technical.rsi >= RSI_OVERBOUGHT:
                alerts.append(
                    Alert(
                        a.ticker,
                        "rsi_overbought",
                        f"{a.ticker}: RSI {a.technical.rsi:.1f} ≥ {RSI_OVERBOUGHT} (overbought)",
                    )
                )
        if (
            a.dividends
            and a.asset_class not in {"Cripto"}
            and a.dividends.dy >= MIN_DY_THRESHOLD
        ):
            alerts.append(
                Alert(
                    a.ticker,
                    "dy_min",
                    f"{a.ticker}: DY {a.dividends.dy * 100:.1f}% ≥ {MIN_DY_THRESHOLD * 100:.0f}%",
                )
            )
    return alerts
