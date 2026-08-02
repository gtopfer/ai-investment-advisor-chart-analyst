from __future__ import annotations

from copy import deepcopy
from typing import Any

from config.config import (
    DEFAULT_BROKERAGE_PCT,
    DEFAULT_IR_PCT,
    STRATEGY_WEIGHTS,
)
from models.schemas import AssetAnalysis


def score_assets(
    assets: list[AssetAnalysis],
    strategy: str,
    weights: dict[str, float] | None = None,
) -> list[AssetAnalysis]:
    """
    Calcula scores e ordena ativos. SPEC-019: preenche score_breakdown.
    """
    w = weights or STRATEGY_WEIGHTS.get(strategy, STRATEGY_WEIGHTS["Equilíbrio"])
    w_tech = float(w.get("technical", 0.5))
    w_div = float(w.get("dividend", 0.5))

    for asset in assets:
        breakdown: dict[str, float] = {
            "base": 0.5,
            "rsi": 0.0,
            "macd": 0.0,
            "ema": 0.0,
            "ai": 0.0,
            "dividend": 0.0,
        }
        tech_score = 0.5
        if asset.technical:
            rsi_component = ((50.0 - asset.technical.rsi) / 50.0) * 0.2
            rsi_component = max(-0.2, min(0.2, rsi_component))
            breakdown["rsi"] = rsi_component
            tech_score += rsi_component

            if asset.technical.macd_signal == "bullish":
                breakdown["macd"] = 0.2
                tech_score += 0.2
            elif asset.technical.macd_signal == "bearish":
                breakdown["macd"] = -0.2
                tech_score -= 0.2

            if asset.technical.ema_trend == "uptrend":
                breakdown["ema"] = 0.2
                tech_score += 0.2
            elif asset.technical.ema_trend == "downtrend":
                breakdown["ema"] = -0.2
                tech_score -= 0.2

            if asset.ai_analysis:
                if asset.ai_analysis.trend == "Bullish":
                    ai_c = asset.ai_analysis.confidence_score * 0.2
                    breakdown["ai"] = ai_c
                    tech_score += ai_c
                elif asset.ai_analysis.trend == "Bearish":
                    ai_c = -asset.ai_analysis.confidence_score * 0.2
                    breakdown["ai"] = ai_c
                    tech_score += ai_c

        asset.technical_score = max(0.0, min(1.0, tech_score))
        div_score = 0.0
        if asset.dividends:
            div_score = asset.dividends.dividend_score
        asset.dividend_score = div_score
        breakdown["dividend"] = div_score

        is_crypto = (
            (asset.asset_class or "").lower() in {"cripto", "crypto"}
            or (asset.market or "").upper() == "CRYPTO"
        )
        if is_crypto:
            asset.total_score = asset.technical_score
            strategy_note = "Score técnico (cripto; dividendos não aplicáveis). "
        else:
            asset.total_score = (asset.technical_score * w_tech) + (asset.dividend_score * w_div)
            strategy_note = ""

        asset.score_breakdown = breakdown
        ai_note = asset.ai_analysis.short_summary_pt if asset.ai_analysis else ""
        if asset.total_score >= 0.6:
            asset.recommendation = "Compra"
            asset.reason = f"{strategy_note}Score alto ({asset.total_score:.2f}). {ai_note}".strip()
        elif asset.total_score <= 0.4:
            asset.recommendation = "Venda/Evitar"
            asset.reason = f"{strategy_note}Score baixo ({asset.total_score:.2f}). {ai_note}".strip()
        else:
            asset.recommendation = "Aguardar"
            asset.reason = (
                f"{strategy_note}Score neutro ({asset.total_score:.2f}). Aguardando definição."
            ).strip()

    return sorted(assets, key=lambda x: x.total_score, reverse=True)


def allocate_capital(
    scored_assets: list[AssetAnalysis],
    total_capital: float,
    max_assets: int = 10,
    class_targets: dict[str, float] | None = None,
) -> list[AssetAnalysis]:
    """
    Distribui capital entre top N.
    SPEC-029: se class_targets (frações 0-1 por classe) somam ~1, aloca por classe
    e dentro da classe por score.
    """
    candidates = [a for a in scored_assets if a.total_score > 0.4][: max(max_assets * 3, max_assets)]
    if not candidates:
        return []

    if class_targets:
        # normaliza targets
        total_t = sum(max(0.0, float(v)) for v in class_targets.values())
        if total_t <= 0:
            class_targets = None
        else:
            class_targets = {k: max(0.0, float(v)) / total_t for k, v in class_targets.items()}

    if not class_targets:
        candidates = candidates[:max_assets]
        total_score_sum = sum(a.total_score for a in candidates)
        for asset in candidates:
            w = asset.total_score / total_score_sum if total_score_sum > 0 else 0.0
            asset.suggested_allocation_pct = w * 100
            asset.suggested_value = total_capital * w
        return candidates

    # por classe
    by_class: dict[str, list[AssetAnalysis]] = {}
    for a in candidates:
        by_class.setdefault(a.asset_class or "Desconhecido", []).append(a)

    selected: list[AssetAnalysis] = []
    for cls, target_frac in class_targets.items():
        bucket = by_class.get(cls, [])
        if not bucket or target_frac <= 0:
            continue
        # pega top por score na classe
        bucket = sorted(bucket, key=lambda x: x.total_score, reverse=True)
        n = max(1, min(len(bucket), max(1, round(max_assets * target_frac))))
        class_cap = total_capital * target_frac
        picks = bucket[:n]
        score_sum = sum(p.total_score for p in picks) or 1.0
        for p in picks:
            w = p.total_score / score_sum
            p.suggested_value = class_cap * w
            selected.append(p)

    # se vazio, fallback
    if not selected:
        return allocate_capital(scored_assets, total_capital, max_assets=max_assets, class_targets=None)

    # normaliza % sobre total_capital
    for p in selected:
        p.suggested_allocation_pct = (
            (p.suggested_value / total_capital * 100.0) if total_capital > 0 else 0.0
        )
    # trim max_assets by value
    selected = sorted(selected, key=lambda x: x.suggested_value, reverse=True)[:max_assets]
    # renormalize values to total_capital
    s = sum(p.suggested_value for p in selected) or 1.0
    for p in selected:
        p.suggested_value = total_capital * (p.suggested_value / s)
        p.suggested_allocation_pct = (
            (p.suggested_value / total_capital * 100.0) if total_capital > 0 else 0.0
        )
    return selected


def build_rebalance_actions(
    current_values: dict[str, float],
    target_assets: list[AssetAnalysis],
    min_trade_value: float = 1.0,
    threshold_pct: float = 0.0,
    target_total: float | None = None,
    brokerage_pct: float = DEFAULT_BROKERAGE_PCT,
    ir_pct: float = DEFAULT_IR_PCT,
) -> list[dict[str, Any]]:
    target_values = {asset.ticker: float(asset.suggested_value) for asset in target_assets}
    if target_total is None:
        target_total = sum(target_values.values())
    target_total = float(target_total or 0.0)

    all_tickers = set(current_values.keys()) | set(target_values.keys())
    actions: list[dict[str, Any]] = []

    for ticker in all_tickers:
        current_value = float(current_values.get(ticker, 0.0))
        target_value = float(target_values.get(ticker, 0.0))
        delta_value = target_value - current_value

        if abs(delta_value) < min_trade_value:
            continue

        if current_value <= 0 and target_value > 0:
            action = "Abrir posição (Comprar)"
        elif target_value <= 0 and current_value > 0:
            action = "Zerar posição (Vender)"
        elif delta_value > 0:
            action = "Comprar mais"
        else:
            action = "Reduzir/Vender"

        deviation_pct = abs(delta_value) / target_total * 100.0 if target_total > 0 else 100.0
        # SPEC-028 custos educacionais
        trade_notional = abs(delta_value)
        brokerage = trade_notional * float(brokerage_pct)
        # IR simplificado só em redução com ganho assumido 0 no MVP se sem cost basis —
        # usa proxy: se vender, IR sobre notional * ir_pct * 0 (sem cost basis) = 0
        # Educacional: aplica IR_pct apenas em vendas como estimativa bruta de atrito
        ir_est = trade_notional * float(ir_pct) * 0.1 if delta_value < 0 else 0.0
        cost_est = brokerage + ir_est

        actions.append(
            {
                "ticker": ticker,
                "action": action,
                "current_value": current_value,
                "target_value": target_value,
                "delta_value": delta_value,
                "deviation_pct": deviation_pct,
                "brokerage_est": brokerage,
                "ir_est": ir_est,
                "cost_est": cost_est,
            }
        )

    actions = sorted(actions, key=lambda item: abs(item["delta_value"]), reverse=True)
    if threshold_pct and threshold_pct > 0:
        actions = [
            item for item in actions if float(item.get("deviation_pct", 0.0)) >= threshold_pct
        ]
    return actions


def build_projected_portfolio(
    current_values: dict[str, float],
    target_assets: list[AssetAnalysis],
) -> list[dict[str, Any]]:
    target_values = {asset.ticker: float(asset.suggested_value) for asset in target_assets}
    target_total = sum(target_values.values())
    all_tickers = set(current_values.keys()) | set(target_values.keys())
    rows: list[dict[str, Any]] = []

    for ticker in sorted(all_tickers):
        current_value = float(current_values.get(ticker, 0.0))
        projected_value = float(target_values.get(ticker, 0.0))
        if current_value <= 0 and projected_value <= 0:
            continue
        pct = (projected_value / target_total * 100.0) if target_total > 0 else 0.0
        delta = projected_value - current_value
        if projected_value <= 0 and current_value > 0:
            status = "Sair"
        elif current_value <= 0 and projected_value > 0:
            status = "Entrar"
        elif abs(delta) < 1.0:
            status = "Manter"
        elif delta > 0:
            status = "Aumentar"
        else:
            status = "Reduzir"

        rows.append(
            {
                "ticker": ticker,
                "current_value": current_value,
                "projected_value": projected_value,
                "projected_pct": pct,
                "delta_value": delta,
                "status": status,
            }
        )

    return sorted(rows, key=lambda r: r["projected_value"], reverse=True)


def projected_positions_for_session(rows: list[dict[str, Any]]) -> dict[str, float]:
    return {
        row["ticker"]: float(row["projected_value"])
        for row in rows
        if float(row.get("projected_value", 0.0)) > 0
    }


def compare_strategies(
    assets: list[AssetAnalysis],
    strategies: list[str],
    total_capital: float,
    max_assets: int = 10,
    weights_override: dict[str, dict[str, float]] | None = None,
) -> dict[str, list[AssetAnalysis]]:
    """SPEC-020: re-score e aloca por estratégia reutilizando a mesma análise."""
    out: dict[str, list[AssetAnalysis]] = {}
    for strat in strategies:
        cloned = deepcopy(assets)
        w = None
        if weights_override and strat in weights_override:
            w = weights_override[strat]
        scored = score_assets(cloned, strat, weights=w)
        out[strat] = allocate_capital(scored, total_capital, max_assets=max_assets)
    return out
