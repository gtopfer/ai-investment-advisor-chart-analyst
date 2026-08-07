from ducks.portfolio.allocator import (
    build_projected_portfolio,
    projected_positions_for_session,
)
from shared.models.schemas import AssetAnalysis, TechnicalIndicators


def _asset(ticker: str, suggested: float) -> AssetAnalysis:
    a = AssetAnalysis(
        ticker=ticker,
        market="BR",
        asset_class="Ações",
        current_price=10.0,
        technical=TechnicalIndicators(
            rsi=50,
            macd_signal="neutral",
            ema_trend="neutral",
            bollinger_position="middle",
            volatility=0.1,
        ),
    )
    a.suggested_value = suggested
    return a


def test_projected_includes_exit_status():
    current = {"PETR4.SA": 4000.0, "VALE3.SA": 2000.0}
    targets = [_asset("PETR4.SA", 5000.0)]
    rows = build_projected_portfolio(current, targets)
    by_ticker = {r["ticker"]: r for r in rows}
    assert by_ticker["PETR4.SA"]["status"] in {"Aumentar", "Manter", "Entrar"}
    assert by_ticker["VALE3.SA"]["status"] == "Sair"
    assert by_ticker["VALE3.SA"]["projected_value"] == 0.0


def test_projected_without_current_uses_targets():
    rows = build_projected_portfolio({}, [_asset("AAPL", 1000.0), _asset("MSFT", 3000.0)])
    assert len(rows) == 2
    assert abs(sum(r["projected_pct"] for r in rows) - 100.0) < 0.01


def test_projected_positions_for_session_excludes_exits():
    rows = [
        {"ticker": "A", "projected_value": 100.0},
        {"ticker": "B", "projected_value": 0.0},
    ]
    pos = projected_positions_for_session(rows)
    assert pos == {"A": 100.0}
