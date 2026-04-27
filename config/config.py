import os

# Configurações Gerais
APP_TITLE = "AI Investment Advisor & Chart Analyst"
APP_ICON = "📈"

# Períodos de Análise
DEFAULT_PERIOD = "1y"
DEFAULT_INTERVAL = "1d"

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
DEFAULT_TICKERS_CRYPTO = ["BTC-USD", "ETH-USD", "SOL-USD"]

# Mapeamento de Classes
ASSET_CLASSES = {
    "Ações": "stock",
    "FIIs": "reit",
    "ETFs": "etf",
    "BDRs": "bdr",
    "Cripto": "crypto"
}

# Chave de API (Tenta pegar do ambiente)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"

# Segurança IA
AI_ACCESS_PASSWORD = os.getenv("AI_ACCESS_PASSWORD", "")
MAX_AI_CALLS_PER_SESSION = int(os.getenv("MAX_AI_CALLS_PER_SESSION", "15"))
