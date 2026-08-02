"""SPEC-013: encode/decode de preferências."""

from portfolio.persistence import DEFAULT_PREFS, decode_prefs, encode_prefs


def test_roundtrip_prefs():
    prefs = {
        **DEFAULT_PREFS,
        "portfolio_text": "PETR4.SA, 1000",
        "capital": 2500.0,
        "rebalance_threshold_pct": 7.5,
        "asset_classes": ["Ações", "BDRs"],
    }
    token = encode_prefs(prefs)
    back = decode_prefs(token)
    assert back is not None
    assert back["portfolio_text"] == "PETR4.SA, 1000"
    assert back["capital"] == 2500.0
    assert back["rebalance_threshold_pct"] == 7.5
    assert "BDRs" in back["asset_classes"]


def test_decode_invalid_returns_none():
    assert decode_prefs(None) is None
    assert decode_prefs("") is None
    assert decode_prefs("%%%not-base64%%%") is None


def test_encode_strips_secrets_if_present():
    token = encode_prefs({**DEFAULT_PREFS, "ai_password": "secret", "api_key": "k"})
    back = decode_prefs(token)
    assert back is not None
    assert "ai_password" not in back
    assert "api_key" not in back
