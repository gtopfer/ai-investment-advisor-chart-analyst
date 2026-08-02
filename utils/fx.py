"""SPEC-016: conversão cambial para moeda-base da carteira."""

from __future__ import annotations

import logging
from collections.abc import Callable

logger = logging.getLogger(__name__)

# Taxa fallback educacional se FX falhar (nunca silenciosa na UI — caller deve avisar)
FALLBACK_USD_BRL = 5.0


def normalize_currency(code: str | None) -> str:
    c = (code or "USD").upper().strip()
    if c in {"BRL", "R$"}:
        return "BRL"
    if c in {"USD", "USDT", "USDC"}:
        return "USD"
    # cripto e outros tratados como USD no MVP
    return "USD"


def convert_amount(
    amount: float,
    from_currency: str,
    to_currency: str,
    usd_brl: float,
) -> float:
    """Converte amount de from_currency para to_currency usando par USD/BRL."""
    src = normalize_currency(from_currency)
    dst = normalize_currency(to_currency)
    if src == dst:
        return float(amount)
    rate = float(usd_brl) if usd_brl and usd_brl > 0 else FALLBACK_USD_BRL
    if src == "USD" and dst == "BRL":
        return float(amount) * rate
    if src == "BRL" and dst == "USD":
        return float(amount) / rate
    return float(amount)


def fetch_usd_brl_rate(
    fetcher: Callable[[], float] | None = None,
) -> tuple[float, bool]:
    """
    Retorna (taxa USD→BRL, ok).
    ok=False se usou fallback.
    """
    if fetcher is not None:
        try:
            rate = float(fetcher())
            if rate > 0:
                return rate, True
        except Exception:
            logger.exception("FX fetcher falhou")
            return FALLBACK_USD_BRL, False

    try:
        import yfinance as yf

        t = yf.Ticker("USDBRL=X")
        hist = t.history(period="5d")
        if hist is not None and not hist.empty:
            rate = float(hist["Close"].iloc[-1])
            if rate > 0:
                return rate, True
        info = getattr(t, "info", {}) or {}
        rate = float(info.get("regularMarketPrice") or info.get("previousClose") or 0)
        if rate > 0:
            return rate, True
    except Exception:
        logger.exception("Falha ao obter USDBRL=X")
    return FALLBACK_USD_BRL, False
