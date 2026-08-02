"""SPEC-012: export CSV."""

from models.schemas import AssetAnalysis, TechnicalIndicators
from portfolio.export_csv import portfolio_target_to_csv, rebalance_actions_to_csv


def _asset(ticker: str, value: float = 1000.0) -> AssetAnalysis:
    a = AssetAnalysis(
        ticker=ticker,
        market="BR",
        asset_class="Ações",
        current_price=10.0,
        technical=TechnicalIndicators(
            rsi=50.0,
            macd_signal="neutral",
            ema_trend="neutral",
            bollinger_position="middle",
            volatility=0.1,
        ),
    )
    a.suggested_value = value
    a.suggested_allocation_pct = 50.0
    a.total_score = 0.7
    a.recommendation = "Compra"
    a.reason = "ok"
    return a


def test_portfolio_target_to_csv_has_header_and_rows():
    csv_text = portfolio_target_to_csv([_asset("PETR4.SA"), _asset("VALE3.SA")])
    assert "ticker" in csv_text.splitlines()[0]
    assert "PETR4.SA" in csv_text
    assert "VALE3.SA" in csv_text


def test_rebalance_actions_to_csv():
    actions = [
        {
            "ticker": "AAPL",
            "action": "Comprar mais",
            "current_value": 100.0,
            "target_value": 500.0,
            "delta_value": 400.0,
            "deviation_pct": 4.0,
        }
    ]
    csv_text = rebalance_actions_to_csv(actions)
    assert "desvio_pct_carteira" in csv_text
    assert "AAPL" in csv_text
    assert "400.00" in csv_text
