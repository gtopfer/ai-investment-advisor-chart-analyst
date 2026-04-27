import pandas as pd
import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from data_fetcher.market_data import get_price_history, get_fundamentals
import streamlit as st

@pytest.fixture(autouse=True)
def clear_caches():
    st.cache_data.clear()

@pytest.fixture
def mock_yf_ticker(mocker):
    return mocker.patch("data_fetcher.market_data.yf.Ticker")

def test_get_price_history_success(mock_yf_ticker):
    dates = pd.date_range("2023-01-01", periods=5)
    mock_df = pd.DataFrame({"Close": [10, 11, 12, 13, 14]}, index=dates)
    mock_ticker_instance = mock_yf_ticker.return_value
    mock_ticker_instance.history.return_value = mock_df

    result_df = get_price_history("TEST", "1mo")

    mock_yf_ticker.assert_called_once_with("TEST")
    mock_ticker_instance.history.assert_called_once_with(period="1mo")
    pd.testing.assert_frame_equal(result_df, mock_df)

def test_get_price_history_empty(mock_yf_ticker):
    mock_ticker_instance = mock_yf_ticker.return_value
    mock_ticker_instance.history.return_value = pd.DataFrame()

    result_df = get_price_history("TEST", "1mo")

    assert result_df.empty
    mock_ticker_instance.history.assert_called_once_with(period="1mo")

def test_get_price_history_exception(mock_yf_ticker, capsys):
    mock_ticker_instance = mock_yf_ticker.return_value
    mock_ticker_instance.history.side_effect = Exception("API Error")

    result_df = get_price_history("TEST", "1mo")

    assert result_df.empty
    captured = capsys.readouterr()
    assert "Erro ao buscar dados para TEST: API Error" in captured.out

def test_get_fundamentals_success(mock_yf_ticker):
    mock_info = {
        "currentPrice": 150.0,
        "marketCap": 1000000,
        "dividendYield": 0.05,
        "trailingPE": 15.5,
        "forwardPE": 14.0,
        "averageVolume": 50000,
        "currency": "BRL",
        "longName": "Test Company"
    }
    mock_ticker_instance = mock_yf_ticker.return_value
    type(mock_ticker_instance).info = PropertyMock(return_value=mock_info)

    result = get_fundamentals("TEST")

    expected = {
        "current_price": 150.0,
        "market_cap": 1000000,
        "dividend_yield": 0.05,
        "trailing_pe": 15.5,
        "forward_pe": 14.0,
        "volume_avg": 50000,
        "currency": "BRL",
        "long_name": "Test Company"
    }
    assert result == expected

def test_get_fundamentals_fallback_price(mock_yf_ticker):
    mock_info = {
        "regularMarketPrice": 145.0, # fallback price
        "marketCap": 1000000,
        "dividendYield": 0.05,
        "trailingPE": 15.5,
        "forwardPE": 14.0,
        "averageVolume": 50000,
        "currency": "BRL",
        "longName": "Test Company"
    }
    mock_ticker_instance = mock_yf_ticker.return_value
    type(mock_ticker_instance).info = PropertyMock(return_value=mock_info)

    result = get_fundamentals("TEST")
    assert result["current_price"] == 145.0

def test_get_fundamentals_missing_fields(mock_yf_ticker):
    # Only returning longName and currency
    mock_info = {
        "currency": "BRL",
        "longName": "Test Company"
    }
    mock_ticker_instance = mock_yf_ticker.return_value
    type(mock_ticker_instance).info = PropertyMock(return_value=mock_info)

    result = get_fundamentals("TEST")

    expected = {
        "current_price": 0.0,
        "market_cap": 0,
        "dividend_yield": 0.0,
        "trailing_pe": 0.0,
        "forward_pe": 0.0,
        "volume_avg": 0,
        "currency": "BRL",
        "long_name": "Test Company"
    }
    assert result == expected

def test_get_fundamentals_none_dividend_yield(mock_yf_ticker):
    mock_info = {
        "dividendYield": None,
        "currency": "BRL",
        "longName": "Test Company"
    }
    mock_ticker_instance = mock_yf_ticker.return_value
    type(mock_ticker_instance).info = PropertyMock(return_value=mock_info)

    result = get_fundamentals("TEST")

    assert result["dividend_yield"] == 0.0

def test_get_fundamentals_exception(mock_yf_ticker, capsys):
    mock_ticker_instance = mock_yf_ticker.return_value
    type(mock_ticker_instance).info = PropertyMock(side_effect=Exception("API Error"))

    result = get_fundamentals("TEST")

    assert result == {}
    captured = capsys.readouterr()
    assert "Erro ao buscar fundamentos para TEST: API Error" in captured.out


# Testes adicionais usando __wrapped__ para validar lógica interna sem cache
@patch('yfinance.Ticker')
def test_get_price_history_wrapped_exception(mock_ticker):
    mock_instance = MagicMock()
    mock_instance.history.side_effect = Exception("API Error")
    mock_ticker.return_value = mock_instance

    df = get_price_history.__wrapped__("TICKER", period="1y")

    assert df.empty
    assert isinstance(df, pd.DataFrame)

@patch('yfinance.Ticker')
def test_get_price_history_wrapped_empty(mock_ticker):
    mock_instance = MagicMock()
    mock_instance.history.return_value = pd.DataFrame()
    mock_ticker.return_value = mock_instance

    df = get_price_history.__wrapped__("TICKER", period="1y")

    assert df.empty
    assert isinstance(df, pd.DataFrame)
