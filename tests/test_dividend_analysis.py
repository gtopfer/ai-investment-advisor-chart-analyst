import pandas as pd
from analysis.dividend_analysis import analyze_dividends
from config.config import MIN_DY_THRESHOLD

def test_analyze_dividends_zero_dy():
    fundamentals = {}
    price_df = pd.DataFrame()

    metrics = analyze_dividends("TEST", fundamentals, price_df)

    assert metrics.dy == 0.0
    assert metrics.dividend_score == 0.0
    assert metrics.summary_pt == "Sem dados de dividendos relevantes."
    assert metrics.stability_note == "Indefinida"
    assert metrics.volatility_flag == "medium"

def test_analyze_dividends_below_threshold():
    dy = MIN_DY_THRESHOLD / 2
    fundamentals = {"dividend_yield": dy}
    price_df = pd.DataFrame()

    metrics = analyze_dividends("TEST", fundamentals, price_df)

    assert metrics.dy == dy
    assert metrics.dividend_score == dy / (MIN_DY_THRESHOLD * 2)
    assert metrics.summary_pt == f"DY de {dy:.2%} abaixo do limiar de {MIN_DY_THRESHOLD:.0%}."
    assert metrics.stability_note == "Regular"
    assert metrics.volatility_flag == "medium"

def test_analyze_dividends_above_threshold():
    dy = MIN_DY_THRESHOLD * 1.5
    fundamentals = {"dividend_yield": dy}
    price_df = pd.DataFrame()

    metrics = analyze_dividends("TEST", fundamentals, price_df)

    assert metrics.dy == dy
    assert metrics.dividend_score == dy / (MIN_DY_THRESHOLD * 2)
    assert metrics.summary_pt == f"Bom pagador de dividendos: {dy:.2%}."
    assert metrics.stability_note == "Regular"
    assert metrics.volatility_flag == "medium"

def test_analyze_dividends_max_score():
    dy = MIN_DY_THRESHOLD * 3
    fundamentals = {"dividend_yield": dy}
    price_df = pd.DataFrame()

    metrics = analyze_dividends("TEST", fundamentals, price_df)

    assert metrics.dy == dy
    assert metrics.dividend_score == 1.0
    assert metrics.summary_pt == f"Bom pagador de dividendos: {dy:.2%}."
    assert metrics.stability_note == "Regular"
    assert metrics.volatility_flag == "medium"
