import pandas as pd

from analysis.technical_analysis import analyze_chart_patterns


def test_analyze_chart_patterns_returns_neutral_when_insufficient():
    df = pd.DataFrame({"Close": [], "High": [], "Low": []})

    indicators = analyze_chart_patterns("TEST", df)

    assert indicators.macd_signal == "neutral"
    assert indicators.support_levels == []
    assert indicators.resistance_levels == []


def test_analyze_chart_patterns_detects_uptrend_with_history():
    dates = pd.date_range("2023-01-01", periods=260, freq="D")
    close = pd.Series(range(100, 360), index=dates)
    price_df = pd.DataFrame(
        {
            "Close": close,
            "High": close * 1.01,
            "Low": close * 0.99,
        },
        index=dates,
    )

    indicators = analyze_chart_patterns("TEST", price_df)

    assert indicators.ema_trend == "uptrend"
    assert indicators.support_levels
    assert indicators.resistance_levels
    assert indicators.rsi > 50
