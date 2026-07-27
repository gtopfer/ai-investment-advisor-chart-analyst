"""Importação de carteira atual (CSV/TXT)."""

from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass, field

from utils.tickers import normalize_ticker

# Reuso das regras de parse numérico alinhadas ao app
_TICKER_RE = re.compile(r"^[A-Z0-9.\-]+$")

PORTFOLIO_CSV_TEMPLATE = """ticker,valor
PETR4.SA,3000
HGLG11.SA,2000
AAPL,1500
BTC,0.5
"""


@dataclass
class ImportResult:
    positions: dict[str, float] = field(default_factory=dict)
    imported_count: int = 0
    skipped_count: int = 0
    skip_reasons: list[str] = field(default_factory=list)
    text: str = ""


def _parse_numeric_value(value: str) -> float:
    clean = value.strip().replace("R$", "").replace(" ", "")
    if "," in clean and "." in clean:
        if clean.rfind(",") > clean.rfind("."):
            clean = clean.replace(".", "").replace(",", ".")
        else:
            clean = clean.replace(",", "")
    elif "," in clean:
        clean = clean.replace(".", "").replace(",", ".")
    return float(clean)


def _add_position(
    positions: dict[str, float],
    ticker_raw: str,
    value_raw: str,
    skip_reasons: list[str],
    line_label: str,
) -> tuple[bool, int]:
    ticker = normalize_ticker(ticker_raw)
    if not ticker or not _TICKER_RE.match(ticker):
        skip_reasons.append(f"{line_label}: ticker inválido")
        return False, 1
    try:
        amount = _parse_numeric_value(value_raw)
    except ValueError:
        skip_reasons.append(f"{line_label}: valor inválido")
        return False, 1
    if amount <= 0:
        skip_reasons.append(f"{line_label}: valor <= 0")
        return False, 1
    positions[ticker] = positions.get(ticker, 0.0) + amount
    return True, 0


def parse_portfolio_csv(content: str) -> ImportResult:
    """
    CSV com cabeçalho opcional. Aceita colunas ticker + valor|quantidade|amount|qty
    ou duas colunas sem nome (ticker, número).
    """
    positions: dict[str, float] = {}
    skip_reasons: list[str] = []
    imported = 0
    skipped = 0

    sample = content.lstrip("\ufeff")
    if not sample.strip():
        return ImportResult(skip_reasons=["arquivo vazio"], skipped_count=1)

    try:
        dialect = csv.Sniffer().sniff(sample[:2048], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel

    reader = csv.reader(io.StringIO(sample), dialect)
    rows = list(reader)
    if not rows:
        return ImportResult(skip_reasons=["arquivo vazio"], skipped_count=1)

    start = 0
    ticker_idx, value_idx = 0, 1
    header = [c.strip().lower() for c in rows[0]]
    header_joined = ",".join(header)
    if any(h in header_joined for h in ("ticker", "ativo", "symbol")) or any(
        h in header for h in ("valor", "quantidade", "amount", "qty", "value")
    ):
        start = 1
        ticker_idx = next(
            (i for i, h in enumerate(header) if h in ("ticker", "ativo", "symbol", "papel")),
            0,
        )
        value_idx = next(
            (
                i
                for i, h in enumerate(header)
                if h in ("valor", "quantidade", "amount", "qty", "value", "qtd")
            ),
            1 if len(header) > 1 else 0,
        )

    for offset, row in enumerate(rows[start:], start=start + 1):
        if not row or all(not str(c).strip() for c in row):
            continue
        if len(row) < 2:
            skip_reasons.append(f"linha {offset}: colunas insuficientes")
            skipped += 1
            continue
        ok, sk = _add_position(
            positions,
            str(row[ticker_idx]),
            str(row[value_idx]),
            skip_reasons,
            f"linha {offset}",
        )
        if ok:
            imported += 1
        else:
            skipped += sk

    text = format_positions_as_text(positions)
    return ImportResult(
        positions=positions,
        imported_count=imported,
        skipped_count=skipped,
        skip_reasons=skip_reasons[:20],
        text=text,
    )


def parse_current_portfolio(raw_text: str) -> dict[str, float]:
    """
    Parseia carteira informada pelo usuário (sidebar / texto livre).
    Formatos aceitos por linha: TICKER,VALOR | TICKER:VALOR | TICKER;VALOR
    Fonte única compartilhada com import TXT.
    """
    return parse_portfolio_txt(raw_text).positions


def parse_portfolio_txt(content: str) -> ImportResult:
    """Formato linha a linha da carteira atual (sidebar e import .txt)."""
    positions: dict[str, float] = {}
    skip_reasons: list[str] = []
    imported = 0
    skipped = 0

    for i, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in re.split(r"[,;:]", line, maxsplit=1) if part.strip()]
        if len(parts) != 2:
            skip_reasons.append(f"linha {i}: formato inválido")
            skipped += 1
            continue
        ok, sk = _add_position(positions, parts[0], parts[1], skip_reasons, f"linha {i}")
        if ok:
            imported += 1
        else:
            skipped += sk

    return ImportResult(
        positions=positions,
        imported_count=imported,
        skipped_count=skipped,
        skip_reasons=skip_reasons[:20],
        text=format_positions_as_text(positions),
    )


def format_positions_as_text(positions: dict[str, float]) -> str:
    lines = []
    for ticker, amount in positions.items():
        if amount == int(amount):
            lines.append(f"{ticker}, {int(amount)}")
        else:
            lines.append(f"{ticker}, {amount}")
    return "\n".join(lines)


def import_portfolio_file(filename: str, content: str | bytes) -> ImportResult:
    if isinstance(content, bytes):
        content = content.decode("utf-8-sig", errors="replace")
    name = (filename or "").lower()
    if name.endswith(".csv"):
        return parse_portfolio_csv(content)
    if name.endswith((".txt", ".tsv")):
        if name.endswith(".tsv"):
            return parse_portfolio_csv(content)
        return parse_portfolio_txt(content)
    # fallback: tenta CSV, se zero importados tenta TXT
    csv_result = parse_portfolio_csv(content)
    if csv_result.imported_count > 0:
        return csv_result
    return parse_portfolio_txt(content)
