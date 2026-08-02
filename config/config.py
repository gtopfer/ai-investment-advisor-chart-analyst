import os

# Configurações Gerais
APP_TITLE = "AI Investment Advisor & Chart Analyst"
APP_ICON = "📈"

# Classes expostas no multiselect da sidebar (fonte única)
# SPEC-008 removeu BDRs mortos; SPEC-014 reintroduz com lista real
ASSET_CLASS_OPTIONS = ["Ações", "FIIs", "ETFs", "BDRs", "Cripto"]

# Períodos de Análise
DEFAULT_PERIOD = "1y"

# Threshold padrão de rebalance (SPEC-015) — % do patrimônio alvo
DEFAULT_REBALANCE_THRESHOLD_PCT = 5.0

# Pesos Padrão para Estratégias (Técnico, Dividendos)
STRATEGY_WEIGHTS = {
    "Growth": {"technical": 0.8, "dividend": 0.2},
    "Dividendos": {"technical": 0.3, "dividend": 0.7},
    "Equilíbrio": {"technical": 0.5, "dividend": 0.5}
}

# Limiares
MIN_DY_THRESHOLD = 0.06  # 6% ao ano
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# Tickers de Exemplo (Fallback)
DEFAULT_TICKERS_BR_STOCKS = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "WEGE3.SA", "BBAS3.SA"]
DEFAULT_TICKERS_BR_FIIS = ["HGLG11.SA", "KNRI11.SA", "MXRF11.SA", "VISC11.SA"]
DEFAULT_TICKERS_US_STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
DEFAULT_TICKERS_US_ETFS = ["SPY", "QQQ"]
DEFAULT_TICKERS_US = DEFAULT_TICKERS_US_STOCKS + DEFAULT_TICKERS_US_ETFS
DEFAULT_TICKERS_CRYPTO = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "BNB-USD",
    "XRP-USD",
    "ADA-USD",
    "AVAX-USD",
    "DOGE-USD",
    "DOT-USD",
    "LINK-USD",
]
# BDRs líquidos B3 (yfinance) — SPEC-014
DEFAULT_TICKERS_BR_BDRS = [
    "AAPL34.SA",
    "MSFT34.SA",
    "GOGL34.SA",
    "AMZO34.SA",
    "NVDC34.SA",
    "TSLA34.SA",
    "META34.SA",
]

# Chaves / modelos de LLM (env)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Preferência de provedor: groq | openai_compatible (vazio = auto)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "")

# Segurança IA
AI_ACCESS_PASSWORD = os.getenv("AI_ACCESS_PASSWORD", "")
MAX_AI_CALLS_PER_SESSION = int(os.getenv("MAX_AI_CALLS_PER_SESSION", "15"))
