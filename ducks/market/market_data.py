"""Wrappers com cache Streamlit sobre o core (SPEC-025)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ducks.market.core import (
    fetch_dividend_history,
    fetch_fundamentals,
    fetch_price_history,
)
from shared.config.config import DEFAULT_PERIOD


@st.cache_data(show_spinner=False, ttl=900)
def get_price_history(ticker: str, period: str = DEFAULT_PERIOD) -> pd.DataFrame:
    return fetch_price_history(ticker, period=period)


@st.cache_data(show_spinner=False, ttl=900)
def get_fundamentals(ticker: str) -> dict:
    return fetch_fundamentals(ticker)


@st.cache_data(show_spinner=False, ttl=900)
def get_dividend_history(ticker: str) -> pd.Series:
    return fetch_dividend_history(ticker)
