import pandas as pd
from typing import Dict
from models.schemas import DividendMetrics
from config.config import MIN_DY_THRESHOLD

def analyze_dividends(ticker: str, fundamentals: Dict, price_df: pd.DataFrame) -> DividendMetrics:
    """
    Analisa métricas de dividendos.
    """
    dy = fundamentals.get("dividend_yield", 0.0)
    
    # Score básico de 0 a 1
    # Se DY > MIN_DY_THRESHOLD (ex: 6%), score aumenta
    # Se DY > 12%, cuidado com armadilha de valor (mas aqui vamos simplificar e dar score alto)
    
    score = 0.0
    summary = "Sem dados de dividendos relevantes."
    stability = "Indefinida"
    
    if dy > 0:
        # Normalização simples: 6% = 0.5, 12% = 1.0
        score = min(dy / (MIN_DY_THRESHOLD * 2), 1.0)
        
        if dy < MIN_DY_THRESHOLD:
            summary = f"DY de {dy:.2%} abaixo do limiar de {MIN_DY_THRESHOLD:.0%}."
        else:
            summary = f"Bom pagador de dividendos: {dy:.2%}."
            
        stability = "Regular" # Placeholder, precisaria de histórico de dividendos detalhado
    
    # Volatilidade flag
    # Se a volatilidade (calculada fora ou aqui) for alta, flag = high
    # Aqui vamos usar um placeholder ou lógica simples se tivéssemos o histórico
    vol_flag = "medium" 
    
    return DividendMetrics(
        dy=dy,
        dividend_score=score,
        stability_note=stability,
        volatility_flag=vol_flag,
        summary_pt=summary
    )
