
from allocator.portfolio_allocator import (
    allocate_capital,
    compare_strategies,
    score_assets,
)
from models.schemas import AssetAnalysis, TechnicalIndicators


def _a(ticker, cls, rsi=30, macd="bullish", ema="uptrend"):
    return AssetAnalysis(
        ticker=ticker,
        market="BR",
        asset_class=cls,
        current_price=10,
        technical=TechnicalIndicators(rsi, macd, ema, "middle", 0.2),
    )


def test_compare_strategies_returns_all():
    assets = [_a("A", "Ações"), _a("B", "Ações", rsi=80, macd="bearish", ema="downtrend")]
    out = compare_strategies(assets, ["Growth", "Dividendos"], 5000, max_assets=2)
    assert "Growth" in out and "Dividendos" in out


def test_class_targets_allocation():
    assets = [
        _a("A1", "Ações"),
        _a("A2", "Ações"),
        _a("F1", "FIIs"),
    ]
    scored = score_assets(assets, "Equilíbrio")
    port = allocate_capital(
        scored,
        10000,
        max_assets=5,
        class_targets={"Ações": 0.7, "FIIs": 0.3},
    )
    by_cls = {}
    for p in port:
        by_cls[p.asset_class] = by_cls.get(p.asset_class, 0) + p.suggested_value
    assert by_cls.get("Ações", 0) > by_cls.get("FIIs", 0)
