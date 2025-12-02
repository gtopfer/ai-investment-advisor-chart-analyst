from app import build_candidate_tickers, classify_ticker
from config.config import DEFAULT_TICKERS_US_ETFS


def test_build_candidate_tickers_filters_etfs_only():
    tickers = build_candidate_tickers(["ETFs"], "Internacional")

    assert set(DEFAULT_TICKERS_US_ETFS).issubset(set(tickers))
    assert {"AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"}.isdisjoint(set(tickers))


def test_build_candidate_tickers_deduplicates():
    tickers = build_candidate_tickers(["Ações", "ETFs"], "Ambos")

    assert len(tickers) == len(set(tickers))


def test_classify_ticker_handles_known_assets():
    assert classify_ticker("SPY") == ("ETFs", "US")
    assert classify_ticker("PETR4.SA") == ("Ações", "BR")
    assert classify_ticker("BTC-USD")[0] == "Cripto"
