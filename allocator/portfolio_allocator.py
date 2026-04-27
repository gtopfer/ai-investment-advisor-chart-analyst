from typing import Any, Dict, List
from models.schemas import AssetAnalysis
from config.config import STRATEGY_WEIGHTS, RSI_OVERSOLD, RSI_OVERBOUGHT

def score_assets(assets: List[AssetAnalysis], strategy: str) -> List[AssetAnalysis]:
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
            # RSI
            if asset.technical.rsi < RSI_OVERSOLD: tech_score += 0.2
            elif asset.technical.rsi > RSI_OVERBOUGHT: tech_score -= 0.2
            
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
        
        # Score Total Ponderado
        asset.total_score = (asset.technical_score * w_tech) + (asset.dividend_score * w_div)
        
        # Decisão Simples
        if asset.total_score >= 0.6:
            asset.recommendation = "Compra"
            asset.reason = f"Score alto ({asset.total_score:.2f}). " + (asset.ai_analysis.short_summary_pt if asset.ai_analysis else "")
        elif asset.total_score <= 0.4:
            asset.recommendation = "Venda/Evitar"
            asset.reason = f"Score baixo ({asset.total_score:.2f}). " + (asset.ai_analysis.short_summary_pt if asset.ai_analysis else "")
        else:
            asset.recommendation = "Aguardar"
            asset.reason = f"Score neutro ({asset.total_score:.2f}). Aguardando definição."

    # Ordenar por score total decrescente
    return sorted(assets, key=lambda x: x.total_score, reverse=True)

def allocate_capital(scored_assets: List[AssetAnalysis], total_capital: float, max_assets: int = 10) -> List[AssetAnalysis]:
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
    current_values: Dict[str, float],
    target_assets: List[AssetAnalysis],
    min_trade_value: float = 1.0,
) -> List[Dict[str, Any]]:
    """
    Compara carteira atual vs. carteira alvo e retorna ações de rebalanceamento.
    """
    target_values = {asset.ticker: float(asset.suggested_value) for asset in target_assets}
    all_tickers = set(current_values.keys()) | set(target_values.keys())
    actions: List[Dict[str, Any]] = []

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

        actions.append(
            {
                "ticker": ticker,
                "action": action,
                "current_value": current_value,
                "target_value": target_value,
                "delta_value": delta_value,
            }
        )

    return sorted(actions, key=lambda item: abs(item["delta_value"]), reverse=True)
