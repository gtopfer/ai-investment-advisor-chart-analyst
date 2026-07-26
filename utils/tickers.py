"""Normalização e heurísticas de tickers (foco em cripto Yahoo Finance)."""

from __future__ import annotations

import re

# Símbolos base conhecidos → forma canônica yfinance
_CRYPTO_BASE_ALIASES: dict[str, str] = {
    "BTC": "BTC-USD",
    "BITCOIN": "BTC-USD",
    "ETH": "ETH-USD",
    "ETHEREUM": "ETH-USD",
    "SOL": "SOL-USD",
    "SOLANA": "SOL-USD",
    "BNB": "BNB-USD",
    "XRP": "XRP-USD",
    "ADA": "ADA-USD",
    "AVAX": "AVAX-USD",
    "DOGE": "DOGE-USD",
    "DOT": "DOT-USD",
    "LINK": "LINK-USD",
    "MATIC": "MATIC-USD",
    "POL": "POL-USD",
    "LTC": "LTC-USD",
    "ATOM": "ATOM-USD",
    "NEAR": "NEAR-USD",
    "UNI": "UNI-USD",
}

_CRYPTO_PAIR_RE = re.compile(r"^[A-Z0-9]{2,15}-USD$")
_CRYPTO_COMPACT_RE = re.compile(r"^([A-Z0-9]{2,12})USD$")


def normalize_ticker(raw: str) -> str:
    """
    Normaliza ticker para forma usada no Yahoo Finance.
    Exemplos: btc → BTC-USD, ethusd → ETH-USD, PETR4.SA → PETR4.SA
    """
    if raw is None:
        return ""
    ticker = str(raw).strip().upper()
    if not ticker:
        return ""
    # Espaços internos (ex.: "BAD TICKER") são inválidos — não colapsar
    if any(ch.isspace() for ch in ticker):
        return ""
    ticker = ticker.replace(" ", "")

    if ticker in _CRYPTO_BASE_ALIASES:
        return _CRYPTO_BASE_ALIASES[ticker]

    if _CRYPTO_PAIR_RE.match(ticker):
        return ticker

    compact = _CRYPTO_COMPACT_RE.match(ticker)
    if compact:
        base = compact.group(1)
        if base in _CRYPTO_BASE_ALIASES:
            return _CRYPTO_BASE_ALIASES[base]
        return f"{base}-USD"

    # BTC/USD ou BTC_USD
    for sep in ("/", "_"):
        if sep in ticker:
            left, _, right = ticker.partition(sep)
            if right in {"USD", "USDT", "USDC"} and left:
                if left in _CRYPTO_BASE_ALIASES:
                    return _CRYPTO_BASE_ALIASES[left]
                return f"{left}-USD"

    return ticker


def is_crypto_ticker(ticker: str) -> bool:
    """True se o ticker (já preferencialmente normalizado) parece cripto Yahoo."""
    t = normalize_ticker(ticker)
    if t in _CRYPTO_BASE_ALIASES.values():
        return True
    if _CRYPTO_PAIR_RE.match(t):
        return True
    base = t.replace("-USD", "") if t.endswith("-USD") else t
    return base in _CRYPTO_BASE_ALIASES
