from unittest.mock import MagicMock

import pytest

import ducks.analysis.ai_chart_engine as engine
from ducks.analysis.ai_chart_engine import (
    _fallback_result,
    _parse_ai_response,
    run_ai_technical_analysis,
)
from shared.models.schemas import TechnicalIndicators


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


def test_run_ai_without_provider_returns_fallback(monkeypatch):
    monkeypatch.setattr(engine, "resolve_default_provider_id", lambda: None)
    result = run_ai_technical_analysis("PETR4.SA", _base_indicators())
    assert result.trend == "Neutral"
    assert "provedor" in result.short_summary_pt.lower() or "configurado" in result.short_summary_pt.lower()


def test_run_ai_uses_injected_provider(monkeypatch):
    mock_provider = MagicMock()
    mock_provider.complete_chat.return_value = (
        '{"trend":"Bearish","short_summary_pt":"Pressão vendedora.","confidence_score":0.7,'
        '"support_levels":[9.0],"resistance_levels":[11.0]}'
    )
    monkeypatch.setattr(engine, "create_provider", lambda _pid: mock_provider)
    monkeypatch.setattr(engine, "resolve_default_provider_id", lambda: "groq")
    monkeypatch.setattr(engine, "default_model_for", lambda _pid: "llama-test")

    result = run_ai_technical_analysis(
        "VALE3.SA",
        _base_indicators(),
        provider_id="groq",
        model="llama-test",
    )

    assert result.trend == "Bearish"
    assert result.confidence_score == pytest.approx(0.7)
    mock_provider.complete_chat.assert_called_once()
