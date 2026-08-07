"""Classificação de tickers e montagem do universo candidato (domínio puro)."""

from __future__ import annotations

import re

from shared.config.config import (
    DEFAULT_TICKERS_BR_BDRS,
    DEFAULT_TICKERS_BR_FIIS,
    DEFAULT_TICKERS_BR_STOCKS,
    DEFAULT_TICKERS_CRYPTO,
    DEFAULT_TICKERS_US,
    DEFAULT_TICKERS_US_ETFS,
    DEFAULT_TICKERS_US_STOCKS,
)
from shared.utils.tickers import is_crypto_ticker, normalize_ticker

_BR_FII_SUFFIX_PATTERN = re.compile(r"1[12]B?\.SA$")
# BDRs comuns: 4 letras + 34/35 + .SA (ex. AAPL34.SA)
_BR_BDR_PATTERN = re.compile(r"^[A-Z]{3,5}3[45]\.SA$")
_US_STOCK_PATTERN = re.compile(r"^[A-Z]{1,5}$")


def classify_ticker(ticker: str) -> tuple[str, str]:
    """
    Best-effort classificação de classe e mercado com base em heurísticas simples.
    Ativos fora das listas padrão (ex.: digitados manualmente na carteira atual)
    caem nos fallbacks por padrão de sufixo/formato antes de "Desconhecido".
    """
    ticker = normalize_ticker(ticker)
    if ticker in DEFAULT_TICKERS_BR_BDRS or _BR_BDR_PATTERN.match(ticker):
        return "BDRs", "BR"
    if ticker in DEFAULT_TICKERS_BR_FIIS:
        return "FIIs", "BR"
    if ticker in DEFAULT_TICKERS_BR_STOCKS:
        return "Ações", "BR"
    if ticker in DEFAULT_TICKERS_US_ETFS:
        return "ETFs", "US"
    if ticker in DEFAULT_TICKERS_US_STOCKS:
        return "Ações", "US"
    if ticker in DEFAULT_TICKERS_US:
        return "Ações/ETF", "US"
    if ticker in DEFAULT_TICKERS_CRYPTO or is_crypto_ticker(ticker):
        return "Cripto", "CRYPTO"
    if ticker.endswith(".SA"):
        if _BR_FII_SUFFIX_PATTERN.search(ticker):
            return "FIIs", "BR"
        return "Ações", "BR"
    if _US_STOCK_PATTERN.match(ticker):
        return "Ações", "US"
    return "Desconhecido", "US/CRYPTO"


def parse_extra_tickers(raw: str | None) -> list[str]:
    """SPEC-017: parse textarea de tickers extras."""
    if not raw or not str(raw).strip():
        return []
    out: list[str] = []
    for part in re.split(r"[\n,;]+", str(raw)):
        t = normalize_ticker(part.strip())
        if t and re.match(r"^[A-Z0-9.\-]+$", t):
            out.append(t)
    return list(dict.fromkeys(out))


def build_candidate_tickers(
    asset_classes,
    universe,
    extra_tickers: list[str] | None = None,
) -> list[str]:
    """
    Monta lista de tickers respeitando filtro de classes e geografia.
    BDRs (SPEC-014): entram sempre que a classe estiver marcada, independente do universo.
    SPEC-017: extra_tickers mesclados com dedupe.
    """
    tickers: list[str] = []

    if universe in ["Nacional", "Ambos"]:
        if "Ações" in asset_classes:
            tickers.extend(DEFAULT_TICKERS_BR_STOCKS)
        if "FIIs" in asset_classes:
            tickers.extend(DEFAULT_TICKERS_BR_FIIS)

    if universe in ["Internacional", "Ambos"]:
        if "Ações" in asset_classes:
            tickers.extend(DEFAULT_TICKERS_US_STOCKS)
        if "ETFs" in asset_classes:
            tickers.extend(DEFAULT_TICKERS_US_ETFS)

    if "BDRs" in asset_classes:
        tickers.extend(DEFAULT_TICKERS_BR_BDRS)

    if "Cripto" in asset_classes:
        tickers.extend(DEFAULT_TICKERS_CRYPTO)

    if extra_tickers:
        tickers.extend(extra_tickers)

    return list(dict.fromkeys(tickers))
