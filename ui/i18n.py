"""SPEC-035: strings PT/EN mínimas."""

from __future__ import annotations

STRINGS = {
    "pt": {
        "subtitle": "Análise técnica, dividendos e alocação — uso educacional",
        "empty_title": "Comece pela barra lateral",
        "empty_steps": (
            "1. Ajuste classes, universo, estratégia e capital<br/>"
            "2. Informe ou importe a carteira atual (opcional)<br/>"
            "3. Clique em <strong>Gerar carteira recomendada</strong>"
        ),
        "generate": "Gerar carteira recomendada",
        "disclaimer": (
            "Aviso legal. Ferramenta de finalidade estritamente educacional. "
            "Os dados não constituem recomendação de compra ou venda. "
            "Rentabilidade passada não garante resultados futuros. "
            "Consulte um profissional certificado antes de investir."
        ),
        "ai_risks": (
            "A análise por IA é probabilística, pode errar e não considera seu perfil "
            "de risco, liquidez nem impostos. Use apenas como material de estudo."
        ),
    },
    "en": {
        "subtitle": "Technical analysis, dividends and allocation — educational use only",
        "empty_title": "Start in the sidebar",
        "empty_steps": (
            "1. Set asset classes, universe, strategy and capital<br/>"
            "2. Enter or import your current portfolio (optional)<br/>"
            "3. Click <strong>Generate recommended portfolio</strong>"
        ),
        "generate": "Generate recommended portfolio",
        "disclaimer": (
            "Legal notice. Educational tool only. Nothing here is investment advice. "
            "Past performance does not guarantee future results. "
            "Consult a licensed professional before investing."
        ),
        "ai_risks": (
            "AI analysis is probabilistic, can be wrong, and does not consider your risk "
            "profile, liquidity or taxes. Use for learning only."
        ),
    },
}


def t(key: str, lang: str = "pt") -> str:
    lang = lang if lang in STRINGS else "pt"
    return STRINGS[lang].get(key, STRINGS["pt"].get(key, key))
