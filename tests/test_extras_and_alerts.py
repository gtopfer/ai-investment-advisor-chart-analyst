from models.schemas import AssetAnalysis, DividendMetrics, TechnicalIndicators
from portfolio.alerts import evaluate_alerts
from portfolio.candidates import build_candidate_tickers, parse_extra_tickers


def test_parse_extra_tickers():
    assert parse_extra_tickers("petr4.sa\nAAPL, MSFT") == ["PETR4.SA", "AAPL", "MSFT"]
    assert parse_extra_tickers("") == []


def test_build_candidates_merges_extras():
    tickers = build_candidate_tickers(["Ações"], "Nacional", extra_tickers=["XYZ.SA"])
    assert "PETR4.SA" in tickers
    assert "XYZ.SA" in tickers


def test_alerts_rsi_oversold():
    asset = AssetAnalysis(
        ticker="X",
        market="BR",
        asset_class="Ações",
        current_price=10,
        technical=TechnicalIndicators(
            rsi=20,
            macd_signal="neutral",
            ema_trend="neutral",
            bollinger_position="middle",
            volatility=0.1,
        ),
        dividends=DividendMetrics(0.08, 0.8, "ok", "low", "ok"),
    )
    alerts = evaluate_alerts([asset])
    assert any(a.rule == "rsi_oversold" for a in alerts)
