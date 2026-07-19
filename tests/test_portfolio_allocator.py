from allocator.portfolio_allocator import allocate_capital, score_assets
from models.schemas import AIAnalysisResult, AssetAnalysis, TechnicalIndicators


def _fake_indicators(rsi: float = 30.0, macd_signal: str = "bullish", ema_trend: str = "uptrend") -> TechnicalIndicators:
    return TechnicalIndicators(
        rsi=rsi,
        macd_signal=macd_signal,
        ema_trend=ema_trend,
        bollinger_position="middle",
        volatility=0.2,
        support_levels=[],
        resistance_levels=[],
    )


def test_score_assets_uses_ai_boost():
    asset = AssetAnalysis(
        ticker="TEST1",
        market="BR",
        asset_class="Ações",
        current_price=10.0,
        technical=_fake_indicators(rsi=25.0),
        ai_analysis=AIAnalysisResult(
            trend="Bullish",
            short_summary_pt="Tendência de alta.",
            confidence_score=0.8,
            support_levels=[],
            resistance_levels=[],
        ),
    )

    scored = score_assets([asset], strategy="Growth")[0]

    assert scored.technical_score > 0.5
    assert scored.total_score >= scored.dividend_score
    assert scored.recommendation in {"Compra", "Aguardar", "Venda/Evitar"}


def test_score_assets_rsi_contribution_is_proportional():
    # Antes, qualquer RSI < 30 (RSI_OVERSOLD) dava o mesmo bônus fixo de +0.2.
    # RSI 20 (bem mais sobrevendido) deve pontuar mais que RSI 29 agora.
    deeply_oversold = AssetAnalysis(
        ticker="DEEP",
        market="BR",
        asset_class="Ações",
        current_price=10.0,
        technical=_fake_indicators(rsi=20.0, macd_signal="neutral", ema_trend="neutral"),
    )
    barely_oversold = AssetAnalysis(
        ticker="BARELY",
        market="BR",
        asset_class="Ações",
        current_price=10.0,
        technical=_fake_indicators(rsi=29.0, macd_signal="neutral", ema_trend="neutral"),
    )

    scored = score_assets([deeply_oversold, barely_oversold], strategy="Growth")
    scores_by_ticker = {a.ticker: a.technical_score for a in scored}

    assert scores_by_ticker["DEEP"] > scores_by_ticker["BARELY"]


def test_allocate_capital_normalizes_weights():
    asset_1 = AssetAnalysis(
        ticker="TEST1",
        market="BR",
        asset_class="Ações",
        current_price=10.0,
        technical=_fake_indicators(rsi=28.0),
    )
    asset_2 = AssetAnalysis(
        ticker="TEST2",
        market="US",
        asset_class="ETF",
        current_price=15.0,
        technical=_fake_indicators(rsi=40.0, ema_trend="uptrend"),
    )

    scored = score_assets([asset_1, asset_2], strategy="Growth")
    portfolio = allocate_capital(scored, total_capital=10_000, max_assets=2)

    assert len(portfolio) == 2
    assert abs(sum(a.suggested_value for a in portfolio) - 10_000) < 1e-6
    assert portfolio[0].suggested_value >= portfolio[1].suggested_value
