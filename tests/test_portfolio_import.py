from portfolio.import_portfolio import (
    format_positions_as_text,
    import_portfolio_file,
    parse_current_portfolio,
    parse_portfolio_csv,
    parse_portfolio_txt,
)


def test_parse_csv_with_header():
    content = "ticker,valor\nPETR4.SA,3000\nAAPL,1500.5\n"
    result = parse_portfolio_csv(content)
    assert result.imported_count == 2
    assert result.positions["PETR4.SA"] == 3000
    assert result.positions["AAPL"] == 1500.5
    assert "PETR4.SA" in result.text


def test_parse_csv_skips_invalid_and_counts():
    content = "ticker,valor\nBAD TICKER,10\nAAPL,100\nMSFT,-5\n"
    result = parse_portfolio_csv(content)
    assert result.imported_count == 1
    assert result.skipped_count >= 2
    assert "AAPL" in result.positions


def test_parse_txt_line_format():
    content = "PETR4.SA, 3000\nHGLG11.SA: 2000\n"
    result = parse_portfolio_txt(content)
    assert result.imported_count == 2
    assert result.positions["HGLG11.SA"] == 2000


def test_import_file_csv_by_extension():
    result = import_portfolio_file("carteira.csv", b"ticker,valor\nBBAS3.SA,500\n")
    assert result.imported_count == 1
    assert result.positions["BBAS3.SA"] == 500


def test_import_empty_does_not_invent_positions():
    result = parse_portfolio_csv("")
    assert result.imported_count == 0
    assert result.positions == {}


def test_format_positions_as_text():
    text = format_positions_as_text({"AAPL": 10.0, "MSFT": 20.5})
    assert "AAPL, 10" in text
    assert "MSFT, 20.5" in text


def test_parse_current_portfolio_delegates_to_shared_txt_parser():
    positions = parse_current_portfolio("PETR4.SA, 1000\n# comment\nAAPL34.SA: 500\n")
    assert positions["PETR4.SA"] == 1000
    assert positions["AAPL34.SA"] == 500


def test_single_numeric_parser_source():
    """Não deve haver cópia de _parse_numeric_value em app.py."""
    import app as app_mod
    import portfolio.import_portfolio as port_mod

    assert hasattr(port_mod, "_parse_numeric_value")
    assert not hasattr(app_mod, "_parse_numeric_value")
