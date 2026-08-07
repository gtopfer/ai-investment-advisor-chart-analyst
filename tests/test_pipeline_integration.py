"""SPEC-026: integração com fetch mockado."""

from ducks.portfolio.allocator import allocate_capital, score_assets
from shared.models.schemas import AssetAnalysis, TechnicalIndicators


def test_score_and_allocate_pipeline_mock():
    assets = [
        AssetAnalysis(
            ticker="A",
            market="BR",
            asset_class="Ações",
            current_price=10,
            technical=TechnicalIndicators(25, "bullish", "uptrend", "middle", 0.2),
        ),
        AssetAnalysis(
            ticker="B",
            market="BR",
            asset_class="FIIs",
            current_price=20,
            technical=TechnicalIndicators(70, "bearish", "downtrend", "middle", 0.3),
        ),
    ]
    scored = score_assets(assets, "Growth")
    assert scored[0].score_breakdown
    portfolio = allocate_capital(scored, 10000, max_assets=2)
    assert portfolio
    assert abs(sum(p.suggested_value for p in portfolio) - 10000) < 1e-6
