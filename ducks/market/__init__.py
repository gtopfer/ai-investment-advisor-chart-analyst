"""Duck: market data (fetch de preços, fundamentos, dividendos)."""

from ducks.market.market_data import (
    get_dividend_history,
    get_fundamentals,
    get_price_history,
)

__all__ = [
    "get_dividend_history",
    "get_fundamentals",
    "get_price_history",
]
