from dataclasses import dataclass, field


@dataclass
class TechnicalIndicators:
    rsi: float
    macd_signal: str  # "bullish", "bearish", "neutral"
    ema_trend: str  # "uptrend", "downtrend", "neutral"
    bollinger_position: str  # "upper", "lower", "middle"
    volatility: float
    support_levels: list[float] = field(default_factory=list)
    resistance_levels: list[float] = field(default_factory=list)
    insufficient_history: bool = False


@dataclass
class AIAnalysisResult:
    trend: str
    short_summary_pt: str
    confidence_score: float
    support_levels: list[float]
    resistance_levels: list[float]


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
    market: str  # "BR", "US", "CRYPTO"
    asset_class: str
    current_price: float
    technical: TechnicalIndicators | None = None
    ai_analysis: AIAnalysisResult | None = None
    dividends: DividendMetrics | None = None

    technical_score: float = 0.0
    dividend_score: float = 0.0
    total_score: float = 0.0
    # SPEC-019
    score_breakdown: dict[str, float] = field(default_factory=dict)

    recommendation: str = "Aguardar"
    reason: str = ""
    suggested_allocation_pct: float = 0.0
    suggested_value: float = 0.0

    # SPEC-016 — vazio = inferir de market
    currency: str = ""
    price_in_base: float = 0.0

    # SPEC-031: closes for chart (optional, not always filled)
    close_series: list[float] = field(default_factory=list)
