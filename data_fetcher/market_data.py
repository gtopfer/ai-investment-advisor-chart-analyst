import time

import streamlit as st
import yfinance as yf
import pandas as pd
from typing import Dict, Optional

from config.config import DEFAULT_PERIOD

_RETRY_ATTEMPTS = 2
_RETRY_BACKOFF_SECONDS = 0.3


def _normalize_dividend_yield(value: Optional[float]) -> float:
    """
    yfinance já retornou dividendYield tanto como fração (0.05) quanto,
    em algumas versões/tickers, como percentual puro (5.0). Qualquer
    valor > 1 é tratado como percentual e convertido para fração.
    """
    if value is None:
        return 0.0
    return value / 100.0 if value > 1.0 else float(value)


@st.cache_data(show_spinner=False, ttl=900)
def get_price_history(ticker: str, period: str = DEFAULT_PERIOD) -> pd.DataFrame:
    """
    Busca histórico de preços via yfinance e cacheia para reduzir chamadas.
    Tenta novamente uma vez em caso de falha transitória antes de desistir.
    """
    last_error: Optional[Exception] = None
    for attempt in range(_RETRY_ATTEMPTS):
        try:
            ticker_obj = yf.Ticker(ticker)
            df = ticker_obj.history(period=period)
            if df.empty:
                return pd.DataFrame()
            return df
        except Exception as e:
            last_error = e
            if attempt < _RETRY_ATTEMPTS - 1:
                time.sleep(_RETRY_BACKOFF_SECONDS)

    print(f"Erro ao buscar dados para {ticker}: {last_error}")
    return pd.DataFrame()

@st.cache_data(show_spinner=False, ttl=900)
def get_fundamentals(ticker: str) -> Dict:
    """
    Busca fundamentos básicos via yfinance e cacheia para reduzir latência.
    Tenta novamente uma vez em caso de falha transitória antes de desistir.
    """
    last_error: Optional[Exception] = None
    for attempt in range(_RETRY_ATTEMPTS):
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info

            # Extração segura de dados
            data = {
                "current_price": info.get("currentPrice") or info.get("regularMarketPrice") or 0.0,
                "market_cap": info.get("marketCap", 0),
                "dividend_yield": _normalize_dividend_yield(info.get("dividendYield")),
                "trailing_pe": info.get("trailingPE", 0.0),
                "forward_pe": info.get("forwardPE", 0.0),
                "volume_avg": info.get("averageVolume", 0),
                "currency": info.get("currency", "USD"),
                "long_name": info.get("longName", ticker)
            }

            return data
        except Exception as e:
            last_error = e
            if attempt < _RETRY_ATTEMPTS - 1:
                time.sleep(_RETRY_BACKOFF_SECONDS)

    print(f"Erro ao buscar fundamentos para {ticker}: {last_error}")
    return {}


@st.cache_data(show_spinner=False, ttl=900)
def get_dividend_history(ticker: str) -> pd.Series:
    """
    Busca histórico de proventos pagos via yfinance, usado para avaliar
    consistência de pagamento (ver analysis/dividend_analysis.py).
    """
    last_error: Optional[Exception] = None
    for attempt in range(_RETRY_ATTEMPTS):
        try:
            ticker_obj = yf.Ticker(ticker)
            dividends = ticker_obj.dividends
            return dividends if dividends is not None else pd.Series(dtype=float)
        except Exception as e:
            last_error = e
            if attempt < _RETRY_ATTEMPTS - 1:
                time.sleep(_RETRY_BACKOFF_SECONDS)

    print(f"Erro ao buscar histórico de dividendos para {ticker}: {last_error}")
    return pd.Series(dtype=float)
