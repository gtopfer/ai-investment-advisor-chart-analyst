import pytest

from analysis.ai_chart_engine import _fallback_result, _parse_ai_response
from models.schemas import TechnicalIndicators


def _base_indicators() -> TechnicalIndicators:
    return TechnicalIndicators(
        rsi=50.0,
        macd_signal="neutral",
        ema_trend="neutral",
        bollinger_position="middle",
        volatility=0.1,
        support_levels=[10.0],
        resistance_levels=[12.0],
    )


def test_parse_ai_response_accepts_code_fences():
    text = """```json
    {
        "trend": "Bullish",
        "short_summary_pt": "Pressão compradora ativa.",
        "confidence_score": "0.9",
        "support_levels": [9.5, 10.0],
        "resistance_levels": [12.5]
    }
    ```"""

    result = _parse_ai_response(text, _base_indicators())

    assert result.trend == "Bullish"
    assert result.confidence_score == pytest.approx(0.9)
    assert result.support_levels == [9.5, 10.0]


def test_parse_ai_response_rejects_invalid_json():
    with pytest.raises(ValueError):
        _parse_ai_response("not-json", _base_indicators())


def test_fallback_preserves_support_resistance():
    indicators = _base_indicators()
    result = _fallback_result(indicators, "fallback")

    assert result.short_summary_pt == "fallback"
    assert result.support_levels == indicators.support_levels
    assert result.resistance_levels == indicators.resistance_levels
