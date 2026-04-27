import pandas as pd
from unittest.mock import patch, MagicMock

from data_fetcher.market_data import get_price_history

@patch('yfinance.Ticker')
@patch('builtins.print')
def test_get_price_history_exception_handling(mock_print, mock_ticker):
    # Mock Ticker.history to raise an exception
    mock_ticker_instance = MagicMock()
    mock_ticker_instance.history.side_effect = Exception("API Error")
    mock_ticker.return_value = mock_ticker_instance

    # Call the function
    df = get_price_history.__wrapped__("TICKER", period="1y")

    # Verify the fallback is an empty dataframe
    assert df.empty
    assert isinstance(df, pd.DataFrame)
    mock_print.assert_called_once_with("Erro ao buscar dados para TICKER: API Error")

@patch('yfinance.Ticker')
def test_get_price_history_empty_df(mock_ticker):
    # Mock Ticker.history to return an empty dataframe
    mock_ticker_instance = MagicMock()
    mock_ticker_instance.history.return_value = pd.DataFrame()
    mock_ticker.return_value = mock_ticker_instance

    # Call the function
    df = get_price_history.__wrapped__("TICKER", period="1y")

    # Verify it returns an empty dataframe
    assert df.empty
    assert isinstance(df, pd.DataFrame)

@patch('yfinance.Ticker')
def test_get_price_history_success(mock_ticker):
    # Mock Ticker.history to return a normal dataframe
    mock_ticker_instance = MagicMock()
    dates = pd.date_range("2023-01-01", periods=10, freq="D")
    df_mock = pd.DataFrame(
        {
            "Close": range(100, 110),
        },
        index=dates,
    )
    mock_ticker_instance.history.return_value = df_mock
    mock_ticker.return_value = mock_ticker_instance

    # Call the function
    df = get_price_history.__wrapped__("TICKER", period="1y")

    # Verify it returns the dataframe
    assert not df.empty
    assert len(df) == 10
    pd.testing.assert_frame_equal(df, df_mock)
