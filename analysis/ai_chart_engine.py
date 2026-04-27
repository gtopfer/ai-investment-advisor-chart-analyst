import json
import logging
from json import JSONDecodeError
from typing import Any, Dict

from groq import Groq

from config.config import GROQ_API_KEY, GROQ_MODEL_NAME
from models.schemas import AIAnalysisResult, TechnicalIndicators


def _fallback_result(indicators: TechnicalIndicators, message: str) -> AIAnalysisResult:
    return AIAnalysisResult(
        trend="Neutral",
        short_summary_pt=message,
        confidence_score=0.0,
        support_levels=indicators.support_levels,
        resistance_levels=indicators.resistance_levels,
    )


def _strip_code_fence(text_response: str) -> str:
    if "```json" in text_response:
        return text_response.split("```json", 1)[1].split("```", 1)[0]
    if "```" in text_response:
        return text_response.split("```", 1)[1].split("```", 1)[0]
    return text_response.strip()


def _parse_ai_response(text_response: str, indicators: TechnicalIndicators) -> AIAnalysisResult:
    cleaned = _strip_code_fence(text_response)
    try:
        data: Dict[str, Any] = json.loads(cleaned)
    except JSONDecodeError as exc:
        raise ValueError(f"Resposta não é JSON válido: {exc}") from exc

    trend = data.get("trend", "Neutral")
    short_summary_pt = data.get("short_summary_pt", "Análise inconclusiva.")
    confidence = data.get("confidence_score", 0.0)

    try:
        confidence_score = float(confidence)
    except (TypeError, ValueError):
        confidence_score = 0.0

    return AIAnalysisResult(
        trend=trend if trend in {"Bullish", "Bearish", "Neutral"} else "Neutral",
        short_summary_pt=short_summary_pt,
        confidence_score=max(0.0, min(1.0, confidence_score)),
        support_levels=data.get("support_levels", indicators.support_levels),
        resistance_levels=data.get("resistance_levels", indicators.resistance_levels),
    )


def run_ai_technical_analysis(ticker: str, indicators: TechnicalIndicators) -> AIAnalysisResult:
    """
    Usa a Groq (Llama 3) para interpretar os indicadores técnicos.
    """

    if not GROQ_API_KEY:
        return _fallback_result(
            indicators,
            "Chave de API da Groq não configurada. Análise IA indisponível.",
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
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=500,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
        )

        text_response = completion.choices[0].message.content or "{}"

        return _parse_ai_response(text_response, indicators)

    except Exception as e:
        logging.error(f"Erro na análise de IA para {ticker}", exc_info=e)
        return _fallback_result(
            indicators,
            "Erro ao conectar com o motor de IA (Groq).",
        )
