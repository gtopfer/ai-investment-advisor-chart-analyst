"""SPEC-025: fetch de mercado puro (sem Streamlit)."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import pandas as pd

from shared.config.config import DEFAULT_PERIOD, OFFLINE_MODE

logger = logging.getLogger(__name__)

_RETRY_ATTEMPTS = 2
_RETRY_BACKOFF_SECONDS = 0.3
_FIXTURES_DIR = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "market"


def _normalize_dividend_yield(value: float | None) -> float:
    if value is None:
        return 0.0
    return value / 100.0 if value > 1.0 else float(value)


def _load_fixture(ticker: str) -> dict | None:
    path = _FIXTURES_DIR / f"{ticker.replace('/', '_')}.json"
    if not path.is_file():
        # try generic
        path = _FIXTURES_DIR / "sample.json"
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def fetch_price_history(ticker: str, period: str = DEFAULT_PERIOD) -> pd.DataFrame:
    if OFFLINE_MODE:
        fix = _load_fixture(ticker)
        if fix and "closes" in fix:
            closes = fix["closes"]
            idx = pd.date_range("2024-01-01", periods=len(closes), freq="D")
            return pd.DataFrame(
                {
                    "Close": closes,
                    "High": [c * 1.01 for c in closes],
                    "Low": [c * 0.99 for c in closes],
                    "Open": closes,
                    "Volume": [1_000_000] * len(closes),
                },
                index=idx,
            )
        return pd.DataFrame()

    import yfinance as yf

    last_error: Exception | None = None
    for attempt in range(_RETRY_ATTEMPTS):
        try:
            df = yf.Ticker(ticker).history(period=period)
            return df if df is not None else pd.DataFrame()
        except Exception as e:
            last_error = e
            if attempt < _RETRY_ATTEMPTS - 1:
                time.sleep(_RETRY_BACKOFF_SECONDS * (attempt + 1))
    logger.warning("Erro ao buscar preços %s: %s", ticker, last_error)
    return pd.DataFrame()


def fetch_fundamentals(ticker: str) -> dict:
    if OFFLINE_MODE:
        fix = _load_fixture(ticker)
        if fix and "fundamentals" in fix:
            return dict(fix["fundamentals"])
        return {
            "current_price": 10.0,
            "market_cap": 0,
            "dividend_yield": 0.0,
            "trailing_pe": 0.0,
            "forward_pe": 0.0,
            "volume_avg": 0,
            "currency": "BRL" if ticker.endswith(".SA") else "USD",
            "long_name": ticker,
        }

    import yfinance as yf

    last_error: Exception | None = None
    for attempt in range(_RETRY_ATTEMPTS):
        try:
            info = yf.Ticker(ticker).info or {}
            return {
                "current_price": info.get("currentPrice")
                or info.get("regularMarketPrice")
                or 0.0,
                "market_cap": info.get("marketCap", 0),
                "dividend_yield": _normalize_dividend_yield(info.get("dividendYield")),
                "trailing_pe": info.get("trailingPE", 0.0),
                "forward_pe": info.get("forwardPE", 0.0),
                "volume_avg": info.get("averageVolume", 0),
                "currency": info.get("currency", "USD"),
                "long_name": info.get("longName", ticker),
            }
        except Exception as e:
            last_error = e
            if attempt < _RETRY_ATTEMPTS - 1:
                time.sleep(_RETRY_BACKOFF_SECONDS * (attempt + 1))
    logger.warning("Erro fundamentos %s: %s", ticker, last_error)
    return {}


def fetch_dividend_history(ticker: str) -> pd.Series:
    if OFFLINE_MODE:
        return pd.Series(dtype=float)

    import yfinance as yf

    last_error: Exception | None = None
    for attempt in range(_RETRY_ATTEMPTS):
        try:
            dividends = yf.Ticker(ticker).dividends
            return dividends if dividends is not None else pd.Series(dtype=float)
        except Exception as e:
            last_error = e
            if attempt < _RETRY_ATTEMPTS - 1:
                time.sleep(_RETRY_BACKOFF_SECONDS * (attempt + 1))
    logger.warning("Erro dividendos %s: %s", ticker, last_error)
    return pd.Series(dtype=float)
