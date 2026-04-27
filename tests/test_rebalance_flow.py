from allocator.portfolio_allocator import build_rebalance_actions
from app import convert_positions_to_value_map, parse_current_portfolio
from models.schemas import AssetAnalysis, TechnicalIndicators


def _fake_asset(ticker: str, price: float, suggested_value: float) -> AssetAnalysis:
    asset = AssetAnalysis(
        ticker=ticker,
        market="BR",
        asset_class="Ações",
        current_price=price,
        technical=TechnicalIndicators(
            rsi=50.0,
            macd_signal="neutral",
            ema_trend="neutral",
            bollinger_position="middle",
            volatility=0.1,
        ),
    )
    asset.suggested_value = suggested_value
    return asset


def test_parse_current_portfolio_accepts_multiple_separators():
    raw = """
    PETR4.SA, 3.000,50
    AAPL:1500.25
    BTC-USD; 0,25
    """
    positions = parse_current_portfolio(raw)

    assert positions["PETR4.SA"] == 3000.50
    assert positions["AAPL"] == 1500.25
    assert positions["BTC-USD"] == 0.25


def test_parse_current_portfolio_ignores_invalid_numeric_values():
    raw = """
    PETR4.SA, invalid_value
    AAPL:1500.25
    """
    positions = parse_current_portfolio(raw)

    assert "PETR4.SA" not in positions
    assert positions["AAPL"] == 1500.25


def test_parse_current_portfolio_ignores_invalid_tickers():
    raw = """
    PETR4.SA, 100
    <script>, 200
    DROP TABLE, 300
    INVALID TICKER, 400
    AAPL, 500
    """
    positions = parse_current_portfolio(raw)

    assert "PETR4.SA" in positions
    assert "AAPL" in positions
    assert "<script>" not in positions
    assert "DROP TABLE" not in positions
    assert "INVALID TICKER" not in positions


def test_convert_positions_quantity_mode_uses_current_price():
    positions = {"PETR4.SA": 10, "AAPL": 2}
    assets = [
        _fake_asset("PETR4.SA", 30.0, 0.0),
        _fake_asset("AAPL", 200.0, 0.0),
    ]

    value_map = convert_positions_to_value_map(positions, "Quantidade de cotas/unidades", assets)

    assert value_map["PETR4.SA"] == 300.0
    assert value_map["AAPL"] == 400.0


def test_build_rebalance_actions_flags_buy_and_sell():
    current_values = {"PETR4.SA": 4000.0, "VALE3.SA": 2000.0}
    target_assets = [
        _fake_asset("PETR4.SA", 30.0, 2500.0),
        _fake_asset("AAPL", 200.0, 3500.0),
    ]

    actions = build_rebalance_actions(current_values, target_assets)
    action_map = {item["ticker"]: item["action"] for item in actions}

    assert action_map["PETR4.SA"] == "Reduzir/Vender"
    assert action_map["AAPL"] == "Abrir posição (Comprar)"
    assert action_map["VALE3.SA"] == "Zerar posição (Vender)"
