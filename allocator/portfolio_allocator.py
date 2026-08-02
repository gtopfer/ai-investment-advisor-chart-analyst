from typing import Any

from config.config import STRATEGY_WEIGHTS
from models.schemas import AssetAnalysis


def score_assets(assets: list[AssetAnalysis], strategy: str) -> list[AssetAnalysis]:
    """
    Calcula scores e ordena ativos baseado na estratégia.
    """
    weights = STRATEGY_WEIGHTS.get(strategy, STRATEGY_WEIGHTS["Equilíbrio"])
    w_tech = weights["technical"]
    w_div = weights["dividend"]
    
    for asset in assets:
        # Score Técnico (0-1)
        tech_score = 0.5 # Base neutra
        if asset.technical:
            # RSI: contribuição proporcional à distância do centro neutro (50),
            # em vez de bônus fixo só quando cruza os limiares de sobrecompra/
            # sobrevenda. RSI 25 e RSI 29 (ambos < 30) deixam de pesar igual.
            rsi_component = ((50.0 - asset.technical.rsi) / 50.0) * 0.2
            tech_score += max(-0.2, min(0.2, rsi_component))

            # MACD
            if asset.technical.macd_signal == "bullish": tech_score += 0.2
            elif asset.technical.macd_signal == "bearish": tech_score -= 0.2
            
            # EMA Trend
            if asset.technical.ema_trend == "uptrend": tech_score += 0.2
            elif asset.technical.ema_trend == "downtrend": tech_score -= 0.2
            
            # AI Confidence boost
            if asset.ai_analysis:
                if asset.ai_analysis.trend == "Bullish":
                    tech_score += (asset.ai_analysis.confidence_score * 0.2)
                elif asset.ai_analysis.trend == "Bearish":
                    tech_score -= (asset.ai_analysis.confidence_score * 0.2)
        
        # Clamp tech_score 0-1
        asset.technical_score = max(0.0, min(1.0, tech_score))
        
        # Score Dividendos (0-1)
        div_score = 0.0
        if asset.dividends:
            div_score = asset.dividends.dividend_score
        asset.dividend_score = div_score

        # Cripto: score total só técnico (DY=0 não deve penalizar Equilíbrio/Dividendos)
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

        # Decisão Simples
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

    # Ordenar por score total decrescente
    return sorted(assets, key=lambda x: x.total_score, reverse=True)

def allocate_capital(scored_assets: list[AssetAnalysis], total_capital: float, max_assets: int = 10) -> list[AssetAnalysis]:
    """
    Distribui capital entre os top N ativos.
    """
    # Filtra apenas recomendações de Compra ou Aguardar (se quiser ser agressivo, só Compra)
    # Aqui vamos pegar os top N independente, mas dar peso 0 se for muito ruim
    
    candidates = [a for a in scored_assets if a.total_score > 0.4][:max_assets]
    
    if not candidates:
        return []
        
    total_score_sum = sum(a.total_score for a in candidates)
    
    for asset in candidates:
        if total_score_sum > 0:
            normalized_weight = asset.total_score / total_score_sum
        else:
            normalized_weight = 0
            
        asset.suggested_allocation_pct = normalized_weight * 100
        asset.suggested_value = total_capital * normalized_weight
        
    return candidates


def build_rebalance_actions(
    current_values: dict[str, float],
    target_assets: list[AssetAnalysis],
    min_trade_value: float = 1.0,
    threshold_pct: float = 0.0,
    target_total: float | None = None,
) -> list[dict[str, Any]]:
    """
    Compara carteira atual vs. carteira alvo e retorna ações de rebalanceamento.

    threshold_pct (SPEC-015): desvio mínimo em % do patrimônio alvo para manter a ação.
    Fórmula: |delta| / target_total * 100. Limiar 0 mantém o comportamento anterior
    (só min_trade_value em R$).
    """
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

        deviation_pct = (
            abs(delta_value) / target_total * 100.0 if target_total > 0 else 100.0
        )

        actions.append(
            {
                "ticker": ticker,
                "action": action,
                "current_value": current_value,
                "target_value": target_value,
                "delta_value": delta_value,
                "deviation_pct": deviation_pct,
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
    """
    Monta visão "como deve ficar": atual vs projetado por ticker.
    Inclui posições a zerar (target 0) com status Sair.
    """
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
    """Posições com valor projetado > 0 para aplicar na carteira da sessão."""
    return {
        row["ticker"]: float(row["projected_value"])
        for row in rows
        if float(row.get("projected_value", 0.0)) > 0
    }
