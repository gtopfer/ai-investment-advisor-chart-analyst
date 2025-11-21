from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TechnicalIndicators:
    rsi: float
    macd_signal: str  # "bullish", "bearish", "neutral"
    ema_trend: str    # "uptrend", "downtrend", "neutral"
    bollinger_position: str # "upper", "lower", "middle"
    volatility: float
    support_levels: List[float] = field(default_factory=list)
    resistance_levels: List[float] = field(default_factory=list)

@dataclass
class AIAnalysisResult:
    trend: str
    short_summary_pt: str
    confidence_score: float
    support_levels: List[float]
    resistance_levels: List[float]

@dataclass
class DividendMetrics:
    dy: float
    dividend_score: float
    stability_note: str
    volatility_flag: str
    summary_pt: str

@dataclass
class AssetAnalysis:
    ticker: str
    market: str # "BR", "US", "CRYPTO"
    asset_class: str
    current_price: float
    technical: Optional[TechnicalIndicators] = None
    ai_analysis: Optional[AIAnalysisResult] = None
    dividends: Optional[DividendMetrics] = None
    
    # Scoring results
    technical_score: float = 0.0
    dividend_score: float = 0.0
    total_score: float = 0.0
    
    # Allocation results
    recommendation: str = "Aguardar" # "Compra", "Aguardar"
    reason: str = ""
    suggested_allocation_pct: float = 0.0
    suggested_value: float = 0.0
