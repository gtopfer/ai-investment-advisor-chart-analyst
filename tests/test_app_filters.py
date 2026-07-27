from app import _split_results
from config.config import ASSET_CLASS_OPTIONS, DEFAULT_TICKERS_US_ETFS
from portfolio.candidates import build_candidate_tickers, classify_ticker


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


def test_classify_ticker_fallback_custom_us_stock():
    # "IBM" não está em nenhuma lista padrão de config.py, mas segue o
    # formato usual de ticker de ações US (1-5 letras maiúsculas).
    assert classify_ticker("IBM") == ("Ações", "US")


def test_classify_ticker_fallback_custom_br_fii():
    # FII fora da lista padrão, mas seguindo o padrão de sufixo "11.SA"
    assert classify_ticker("XPML11.SA") == ("FIIs", "BR")


def test_classify_ticker_fallback_custom_br_stock():
    # Ação BR fora da lista padrão, sem o sufixo característico de FII
    assert classify_ticker("RENT3.SA") == ("Ações", "BR")


def test_classify_ticker_unknown_stays_unknown():
    assert classify_ticker("1234") == ("Desconhecido", "US/CRYPTO")


def test_split_results_separates_failed_tickers_preserving_order():
    tickers = ["A", "B", "C"]
    results = {"A": "asset-a", "B": None, "C": "asset-c"}

    analyzed, failed = _split_results(tickers, results)

    assert analyzed == ["asset-a", "asset-c"]
    assert failed == ["B"]


def test_asset_class_options_exclude_bdrs():
    assert "BDRs" not in ASSET_CLASS_OPTIONS
    assert set(ASSET_CLASS_OPTIONS) == {"Ações", "FIIs", "ETFs", "Cripto"}


def test_build_candidate_tickers_bdrs_alone_is_empty():
    # Classe removida da UI; se ainda for passada, não há ramo de candidatos
    assert build_candidate_tickers(["BDRs"], "Ambos") == []
