import yfinance as yf
import pandas as pd
from typing import Dict, Optional

def get_price_history(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Busca histórico de preços via yfinance.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(period=period)
        if df.empty:
            return pd.DataFrame()
        return df
    except Exception as e:
        print(f"Erro ao buscar dados para {ticker}: {e}")
        return pd.DataFrame()

def get_fundamentals(ticker: str) -> Dict:
    """
    Busca fundamentos básicos via yfinance.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        
        # Extração segura de dados
        data = {
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice") or 0.0,
            "market_cap": info.get("marketCap", 0),
            "dividend_yield": info.get("dividendYield", 0.0),
            "trailing_pe": info.get("trailingPE", 0.0),
            "forward_pe": info.get("forwardPE", 0.0),
            "volume_avg": info.get("averageVolume", 0),
            "currency": info.get("currency", "USD"),
            "long_name": info.get("longName", ticker)
        }
        
        # Se dividendYield vier None, assume 0
        if data["dividend_yield"] is None:
            data["dividend_yield"] = 0.0
            
        return data
    except Exception as e:
        print(f"Erro ao buscar fundamentos para {ticker}: {e}")
        return {}
