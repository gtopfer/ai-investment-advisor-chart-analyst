from allocator.portfolio_allocator import score_assets
from analysis.dividend_analysis import analyze_dividends
from app import classify_ticker, parse_current_portfolio
from models.schemas import AssetAnalysis, DividendMetrics, TechnicalIndicators
from portfolio.import_portfolio import parse_portfolio_csv
from utils.tickers import is_crypto_ticker, normalize_ticker


def _tech(**kwargs) -> TechnicalIndicators:
    base = {
        "rsi": 50.0,
        "macd_signal": "bullish",
        "ema_trend": "uptrend",
        "bollinger_position": "middle",
        "volatility": 0.4,
    }
    base.update(kwargs)
    return TechnicalIndicators(**base)


def test_normalize_crypto_aliases():
    assert normalize_ticker("btc") == "BTC-USD"
    assert normalize_ticker("ETH") == "ETH-USD"
    assert normalize_ticker("solusd") == "SOL-USD"
    assert normalize_ticker("BTC-USD") == "BTC-USD"
    assert normalize_ticker("PETR4.SA") == "PETR4.SA"
    assert normalize_ticker("btc/usd") == "BTC-USD"


def test_is_crypto_ticker():
    assert is_crypto_ticker("BTC")
    assert is_crypto_ticker("ETH-USD")
    assert not is_crypto_ticker("AAPL")
    assert not is_crypto_ticker("PETR4.SA")


def test_classify_ticker_crypto_aliases():
    assert classify_ticker("BTC") == ("Cripto", "CRYPTO")
    assert classify_ticker("eth") == ("Cripto", "CRYPTO")
    assert classify_ticker("LINK-USD") == ("Cripto", "CRYPTO")


def test_parse_portfolio_normalizes_crypto():
    positions = parse_current_portfolio("BTC, 1000\nETH, 500\n")
    assert "BTC-USD" in positions
    assert "ETH-USD" in positions
    assert positions["BTC-USD"] == 1000


def test_import_csv_normalizes_crypto():
    result = parse_portfolio_csv("ticker,valor\nBTC,100\nADA,50\n")
    assert result.imported_count == 2
    assert "BTC-USD" in result.positions
    assert "ADA-USD" in result.positions


def test_crypto_score_ignores_dividend_weight():
    """Em estratégia Dividendos, cripto com DY=0 não deve ser esmagada."""
    crypto = AssetAnalysis(
        ticker="BTC-USD",
        market="CRYPTO",
        asset_class="Cripto",
        current_price=60000,
        technical=_tech(),
        dividends=DividendMetrics(
            dy=0.0,
            dividend_score=0.0,
            stability_note="Não aplicável",
            volatility_flag="high",
            summary_pt="n/a",
        ),
    )
    stock = AssetAnalysis(
        ticker="ITUB4.SA",
        market="BR",
        asset_class="Ações",
        current_price=30,
        technical=_tech(macd_signal="neutral", ema_trend="neutral"),
        dividends=DividendMetrics(
            dy=0.08,
            dividend_score=0.7,
            stability_note="Consistente",
            volatility_flag="low",
            summary_pt="ok",
        ),
    )
    scored = score_assets([crypto, stock], "Dividendos")
    by_ticker = {a.ticker: a for a in scored}
    # técnico-only: base 0.5 + macd 0.2 + ema 0.2 = 0.9
    assert by_ticker["BTC-USD"].total_score == by_ticker["BTC-USD"].technical_score
    assert by_ticker["BTC-USD"].total_score >= 0.8
    # ação ainda mistura técnico + dividendo (pesos Dividendos)
    assert by_ticker["ITUB4.SA"].total_score != by_ticker["ITUB4.SA"].technical_score


def test_analyze_dividends_crypto_flag():
    import pandas as pd

    metrics = analyze_dividends(
        "BTC-USD",
        {"dividend_yield": 0.0},
        pd.DataFrame({"Close": [1.0, 2.0, 3.0]}),
        is_crypto=True,
    )
    assert metrics.dividend_score == 0.0
    assert "não se aplicam" in metrics.summary_pt.lower() or "nao se aplicam" in metrics.summary_pt.lower()
