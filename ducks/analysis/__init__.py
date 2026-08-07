"""Duck: análise técnica, dividendos e interpretação por IA."""

from ducks.analysis.ai_chart_engine import run_ai_technical_analysis
from ducks.analysis.dividend_analysis import analyze_dividends
from ducks.analysis.technical_analysis import analyze_chart_patterns

__all__ = [
    "analyze_chart_patterns",
    "analyze_dividends",
    "run_ai_technical_analysis",
]
