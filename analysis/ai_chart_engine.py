import json
import os
from groq import Groq
from models.schemas import AIAnalysisResult, TechnicalIndicators
from config.config import GROQ_API_KEY, GROQ_MODEL_NAME

def run_ai_technical_analysis(ticker: str, indicators: TechnicalIndicators) -> AIAnalysisResult:
    """
    Usa a Groq (Llama 3) para interpretar os indicadores técnicos.
    """
    
    # Fallback se não houver chave
    if not GROQ_API_KEY:
        return AIAnalysisResult(
            trend="Neutral",
            short_summary_pt="Chave de API da Groq não configurada. Análise IA indisponível.",
            confidence_score=0.0,
            support_levels=indicators.support_levels,
            resistance_levels=indicators.resistance_levels
        )

    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        prompt = f"""
        You are a professional Technical Analyst.
        Analyze the following technical indicators for {ticker}:
        
        - RSI: {indicators.rsi:.2f}
        - MACD Signal: {indicators.macd_signal}
        - EMA Trend: {indicators.ema_trend}
        - Bollinger Position: {indicators.bollinger_position}
        - Volatility (Annualized): {indicators.volatility:.2f}
        - Recent Support (approx): {indicators.support_levels}
        - Recent Resistance (approx): {indicators.resistance_levels}
        
        Task:
        1. Classify the trend as Bullish, Bearish, or Neutral.
        2. Provide a short summary in Portuguese (PT-BR) explaining if it's a "Compra" or "Aguardar" scenario.
        3. Assign a confidence score (0.0 to 1.0).
        
        Return ONLY a JSON object with this structure:
        {{
            "trend": "Bullish/Bearish/Neutral",
            "short_summary_pt": "...",
            "confidence_score": 0.8,
            "support_levels": [10.5, 10.0],
            "resistance_levels": [12.0, 12.5]
        }}
        """
        
        completion = client.chat.completions.create(
            model=GROQ_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful financial analyst assistant that outputs only JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"}
        )
        
        text_response = completion.choices[0].message.content
        
        # Limpeza básica do JSON (caso venha com markdown ```json ... ```)
        if "```json" in text_response:
            text_response = text_response.split("```json")[1].split("```")[0]
        elif "```" in text_response:
            text_response = text_response.split("```")[1].split("```")[0]
            
        data = json.loads(text_response)
        
        return AIAnalysisResult(
            trend=data.get("trend", "Neutral"),
            short_summary_pt=data.get("short_summary_pt", "Análise inconclusiva."),
            confidence_score=float(data.get("confidence_score", 0.5)),
            support_levels=data.get("support_levels", indicators.support_levels),
            resistance_levels=data.get("resistance_levels", indicators.resistance_levels)
        )
        
    except Exception as e:
        print(f"Erro na análise de IA para {ticker}: {e}")
        return AIAnalysisResult(
            trend="Neutral",
            short_summary_pt="Erro ao conectar com o motor de IA (Groq).",
            confidence_score=0.0,
            support_levels=indicators.support_levels,
            resistance_levels=indicators.resistance_levels
        )
