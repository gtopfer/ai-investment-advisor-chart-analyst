"""SPEC-010: avisos de qualidade de dados (histórico curto)."""

from app import _tickers_with_insufficient_history
from models.schemas import AssetAnalysis, TechnicalIndicators


def test_tickers_with_insufficient_history_lists_flagged_assets():
    ok = AssetAnalysis(
        ticker="OK",
        market="US",
        asset_class="Ações",
        current_price=1.0,
        technical=TechnicalIndicators(
            rsi=50,
            macd_signal="neutral",
            ema_trend="neutral",
            bollinger_position="middle",
            volatility=0.1,
            insufficient_history=False,
        ),
    )
    short = AssetAnalysis(
        ticker="SHORT",
        market="US",
        asset_class="Ações",
        current_price=1.0,
        technical=TechnicalIndicators(
            rsi=50,
            macd_signal="neutral",
            ema_trend="neutral",
            bollinger_position="middle",
            volatility=0.0,
            insufficient_history=True,
        ),
    )
    assert _tickers_with_insufficient_history([ok, short]) == ["SHORT"]


def test_tickers_with_insufficient_history_empty_when_none():
    asset = AssetAnalysis(
        ticker="A",
        market="US",
        asset_class="Ações",
        current_price=1.0,
        technical=None,
    )
    assert _tickers_with_insufficient_history([asset]) == []
