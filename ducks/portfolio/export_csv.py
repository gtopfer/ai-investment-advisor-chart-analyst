"""SPEC-012: builders de CSV para carteira alvo e plano de rebalance."""

from __future__ import annotations

import csv
import io
from typing import Any

from shared.models.schemas import AssetAnalysis


def portfolio_target_to_csv(portfolio: list[AssetAnalysis]) -> str:
    """CSV da carteira recomendada (alvo)."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(
        [
            "ticker",
            "classe",
            "recomendacao",
            "score",
            "alocacao_pct",
            "valor_simulado",
            "preco",
            "motivo",
        ]
    )
    for p in portfolio:
        writer.writerow(
            [
                p.ticker,
                p.asset_class,
                p.recommendation,
                f"{p.total_score:.4f}",
                f"{p.suggested_allocation_pct:.4f}",
                f"{p.suggested_value:.2f}",
                f"{p.current_price:.6f}",
                (p.reason or "").replace("\n", " "),
            ]
        )
    return buf.getvalue()


def rebalance_actions_to_csv(actions: list[dict[str, Any]]) -> str:
    """CSV do plano de rebalanceamento (já filtrado se threshold aplicado)."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(
        [
            "ticker",
            "acao",
            "valor_atual",
            "valor_alvo",
            "ajuste",
            "desvio_pct_carteira",
        ]
    )
    for item in actions:
        writer.writerow(
            [
                item.get("ticker", ""),
                item.get("action", ""),
                f"{float(item.get('current_value', 0.0)):.2f}",
                f"{float(item.get('target_value', 0.0)):.2f}",
                f"{float(item.get('delta_value', 0.0)):.2f}",
                f"{float(item.get('deviation_pct', 0.0)):.4f}",
            ]
        )
    return buf.getvalue()
