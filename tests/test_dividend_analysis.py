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

def test_analyze_dividends_consistent_history():
    dy = MIN_DY_THRESHOLD * 1.5
    fundamentals = {"dividend_yield": dy}
    price_df = pd.DataFrame()
    dividend_history = pd.Series(
        [0.5, 0.5, 0.5, 0.5, 0.5],
        index=pd.to_datetime(["2021-06-01", "2022-06-01", "2023-06-01", "2024-06-01", "2025-06-01"]),
    )

    metrics = analyze_dividends("TEST", fundamentals, price_df, dividend_history)

    assert metrics.stability_note == "Consistente"

def test_analyze_dividends_irregular_history():
    dy = MIN_DY_THRESHOLD * 1.5
    fundamentals = {"dividend_yield": dy}
    price_df = pd.DataFrame()
    # Pagou só em 2 dos 10 anos observados (2016 e 2025) -> abaixo do limiar de consistência
    dividend_history = pd.Series(
        [0.5, 0.5],
        index=pd.to_datetime(["2016-06-01", "2025-06-01"]),
    )

    metrics = analyze_dividends("TEST", fundamentals, price_df, dividend_history)

    assert metrics.stability_note == "Irregular"

def test_analyze_dividends_insufficient_history():
    dy = MIN_DY_THRESHOLD * 1.5
    fundamentals = {"dividend_yield": dy}
    price_df = pd.DataFrame()
    dividend_history = pd.Series([0.5], index=pd.to_datetime(["2025-06-01"]))

    metrics = analyze_dividends("TEST", fundamentals, price_df, dividend_history)

    assert metrics.stability_note == "Histórico insuficiente"

def test_analyze_dividends_volatility_flag_low_from_price_history():
    dy = MIN_DY_THRESHOLD * 1.5
    fundamentals = {"dividend_yield": dy}
    dates = pd.date_range("2024-01-01", periods=60, freq="D")
    # Preço quase constante -> volatilidade anualizada baixa
    close = pd.Series([100.0 + (i % 2) * 0.01 for i in range(60)], index=dates)
    price_df = pd.DataFrame({"Close": close})

    metrics = analyze_dividends("TEST", fundamentals, price_df)

    assert metrics.volatility_flag == "low"

def test_analyze_dividends_volatility_flag_high_from_price_history():
    dy = MIN_DY_THRESHOLD * 1.5
    fundamentals = {"dividend_yield": dy}
    dates = pd.date_range("2024-01-01", periods=60, freq="D")
    # Alterna alta/baixa forte todo dia -> volatilidade anualizada alta
    close = pd.Series([100.0 if i % 2 == 0 else 70.0 for i in range(60)], index=dates)
    price_df = pd.DataFrame({"Close": close})

    metrics = analyze_dividends("TEST", fundamentals, price_df)

    assert metrics.volatility_flag == "high"

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
