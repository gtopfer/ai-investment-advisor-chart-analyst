import pandas as pd
import pandas_ta as ta
from models.schemas import TechnicalIndicators

def analyze_chart_patterns(ticker: str, price_df: pd.DataFrame) -> TechnicalIndicators:
    """
    Calcula indicadores técnicos usando pandas-ta e retorna um objeto TechnicalIndicators.
    """
    if price_df.empty or len(price_df) < 50:
        # Retorna objeto vazio/neutro se não houver dados suficientes
        return TechnicalIndicators(
            rsi=50.0,
            macd_signal="neutral",
            ema_trend="neutral",
            bollinger_position="middle",
            volatility=0.0
        )

    # 1. RSI
    rsi_series = price_df.ta.rsi(length=14)
    current_rsi = rsi_series.iloc[-1] if not rsi_series.empty else 50.0

    # 2. MACD
    macd = price_df.ta.macd(fast=12, slow=26, signal=9)
    # Colunas usuais: MACD_12_26_9, MACDs_12_26_9, MACDh_12_26_9
    if macd is not None and not macd.empty:
        macd_line = macd.iloc[-1]['MACD_12_26_9']
        signal_line = macd.iloc[-1]['MACDs_12_26_9']
        macd_hist = macd.iloc[-1]['MACDh_12_26_9']
        
        if macd_line > signal_line and macd_hist > 0:
            macd_signal = "bullish"
        elif macd_line < signal_line and macd_hist < 0:
            macd_signal = "bearish"
        else:
            macd_signal = "neutral"
    else:
        macd_signal = "neutral"

    # 3. EMAs
    ema20 = price_df.ta.ema(length=20)
    ema50 = price_df.ta.ema(length=50)
    ema200 = price_df.ta.ema(length=200)
    
    ema_trend = "neutral"
    if ema20 is not None and ema50 is not None and ema200 is not None:
        e20 = ema20.iloc[-1]
        e50 = ema50.iloc[-1]
        e200 = ema200.iloc[-1]
        
        if e20 > e50 > e200:
            ema_trend = "uptrend"
        elif e20 < e50 < e200:
            ema_trend = "downtrend"

    # 4. Bollinger Bands
    bb = price_df.ta.bbands(length=20, std=2)
    # Colunas podem variar conforme a versão (ex: BBL_20_2.0_2.0 vs BBL_20_2.0)
    bollinger_position = "middle"
    if bb is not None and not bb.empty:
        close = price_df['Close'].iloc[-1]
        
        bbu_col = next((col for col in bb.columns if col.startswith('BBU')), None)
        bbl_col = next((col for col in bb.columns if col.startswith('BBL')), None)

        if bbu_col and bbl_col:
            upper = bb.iloc[-1][bbu_col]
            lower = bb.iloc[-1][bbl_col]

            if close >= upper * 0.98: # Próximo da banda superior
                bollinger_position = "upper"
            elif close <= lower * 1.02: # Próximo da banda inferior
                bollinger_position = "lower"

    # 5. Volatilidade recente (20 dias) usando variação percentual diária
    returns = price_df["Close"].pct_change().dropna().tail(20)
    volatility = returns.std() * (252**0.5) if not returns.empty else 0.0

    # 6. Suportes e Resistências (simplificado: máximas e mínimas locais recentes)
    if len(price_df) >= 2:
        recent_window = price_df.tail(60)
        resistance = recent_window["High"].max()
        support = recent_window["Low"].min()
    else:
        last_close = price_df["Close"].iloc[-1]
        resistance = last_close
        support = last_close

    return TechnicalIndicators(
        rsi=float(current_rsi),
        macd_signal=macd_signal,
        ema_trend=ema_trend,
        bollinger_position=bollinger_position,
        volatility=float(volatility) if pd.notna(volatility) else 0.0,
        support_levels=[float(support)] if pd.notna(support) else [],
        resistance_levels=[float(resistance)] if pd.notna(resistance) else []
    )
