"""SPEC-013: serialização de preferências/carteira para persistência no browser (query params)."""

from __future__ import annotations

import base64
import json
from typing import Any

DEFAULT_PORTFOLIO_TEXT = "PETR4.SA, 3000\nHGLG11.SA, 2000\nAAPL, 1500"

DEFAULT_PREFS: dict[str, Any] = {
    "portfolio_text": DEFAULT_PORTFOLIO_TEXT,
    "asset_classes": ["Ações", "FIIs"],
    "universe": "Nacional",
    "strategy": "Equilíbrio",
    "capital": 10000.0,
    "portfolio_mode": "Valor atual (R$)",
    "rebalance_threshold_pct": 5.0,
}

QUERY_KEY = "prefs"


def encode_prefs(prefs: dict[str, Any]) -> str:
    """Serializa preferências em token seguro para URL (base64url JSON)."""
    payload = {**DEFAULT_PREFS, **prefs}
    # Nunca incluir senhas/chaves
    payload.pop("ai_password", None)
    payload.pop("api_key", None)
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return base64.urlsafe_b64encode(raw.encode("utf-8")).decode("ascii")


def decode_prefs(token: str | None) -> dict[str, Any] | None:
    """Decodifica token; None se inválido/vazio."""
    if not token or not str(token).strip():
        return None
    try:
        raw = base64.urlsafe_b64decode(str(token).encode("ascii"))
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, json.JSONDecodeError, UnicodeError):
        return None
    if not isinstance(data, dict):
        return None
    merged = {**DEFAULT_PREFS}
    for key in DEFAULT_PREFS:
        if key in data:
            merged[key] = data[key]
    # normalizações leves
    if not isinstance(merged.get("asset_classes"), list):
        merged["asset_classes"] = list(DEFAULT_PREFS["asset_classes"])
    try:
        merged["capital"] = float(merged["capital"])
    except (TypeError, ValueError):
        merged["capital"] = DEFAULT_PREFS["capital"]
    try:
        merged["rebalance_threshold_pct"] = float(merged["rebalance_threshold_pct"])
    except (TypeError, ValueError):
        merged["rebalance_threshold_pct"] = DEFAULT_PREFS["rebalance_threshold_pct"]
    return merged
