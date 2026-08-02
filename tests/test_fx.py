from utils.fx import convert_amount, fetch_usd_brl_rate, normalize_currency


def test_normalize_currency():
    assert normalize_currency("brl") == "BRL"
    assert normalize_currency("USD") == "USD"
    assert normalize_currency(None) == "USD"


def test_convert_usd_to_brl():
    assert convert_amount(10, "USD", "BRL", 5.0) == 50.0
    assert convert_amount(50, "BRL", "USD", 5.0) == 10.0
    assert convert_amount(10, "BRL", "BRL", 5.0) == 10.0


def test_fetch_rate_fallback_on_bad_fetcher():
    def _boom():
        raise RuntimeError("no fx")

    rate, ok = fetch_usd_brl_rate(fetcher=_boom)
    assert rate > 0
    assert ok is False
