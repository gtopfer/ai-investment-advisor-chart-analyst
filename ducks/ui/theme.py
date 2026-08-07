"""Design tokens + CSS do tema escuro monocromático.

Fonte de verdade documental: `docs/design-system.md` e `system-design.md` §3.
Escala: azul-cinza (quase mono), sem acentos coloridos.
"""

from __future__ import annotations

from typing import Final

# ── Tokens (monocromáticos) ──────────────────────────────────────────────────

# Superfícies (do mais escuro ao mais claro)
COLOR_BG: Final = "#0f1419"
COLOR_BG_ELEVATED: Final = "#121820"
COLOR_SURFACE: Final = "#151b23"

# Bordas / divisores
COLOR_BORDER: Final = "#243041"
COLOR_BORDER_MUTED: Final = "#2a3a4d"

# Texto
COLOR_TEXT: Final = "#e7ecf1"
COLOR_TEXT_HEADING: Final = "#f3f6f9"
COLOR_TEXT_MUTED: Final = "#8b9bb0"
COLOR_TEXT_SUBTLE: Final = "#9aabbf"

# Tipografia
FONT_WEIGHT_HEADING: Final = 600
LETTER_SPACING_HEADING: Final = "-0.02em"
FONT_SIZE_SUBTITLE: Final = "0.95rem"
FONT_SIZE_LEGAL: Final = "0.85rem"

# Espaçamento / raio / layout
RADIUS_CARD: Final = "10px"
RADIUS_EMPTY: Final = "12px"
SPACE_PAGE_TOP: Final = "1.5rem"
SPACE_SECTION: Final = "2rem"
MAX_CONTENT_WIDTH: Final = "1100px"

# Escala completa exportável (para docs/testes)
TOKENS: Final[dict[str, str]] = {
    "color.bg": COLOR_BG,
    "color.bg_elevated": COLOR_BG_ELEVATED,
    "color.surface": COLOR_SURFACE,
    "color.border": COLOR_BORDER,
    "color.border_muted": COLOR_BORDER_MUTED,
    "color.text": COLOR_TEXT,
    "color.text_heading": COLOR_TEXT_HEADING,
    "color.text_muted": COLOR_TEXT_MUTED,
    "color.text_subtle": COLOR_TEXT_SUBTLE,
    "radius.card": RADIUS_CARD,
    "radius.empty": RADIUS_EMPTY,
    "layout.max_width": MAX_CONTENT_WIDTH,
}


def dark_css() -> str:
    """CSS injetado no Streamlit a partir dos tokens nomeados."""
    return f"""
<style>
    .stApp {{
        background-color: {COLOR_BG};
        color: {COLOR_TEXT};
    }}
    [data-testid="stSidebar"] {{
        background-color: {COLOR_SURFACE};
        border-right: 1px solid {COLOR_BORDER};
    }}
    [data-testid="stSidebar"] * {{
        color: {COLOR_TEXT};
    }}
    h1, h2, h3 {{
        color: {COLOR_TEXT_HEADING} !important;
        font-weight: {FONT_WEIGHT_HEADING} !important;
        letter-spacing: {LETTER_SPACING_HEADING};
    }}
    .main-subtitle {{
        color: {COLOR_TEXT_MUTED};
        font-size: {FONT_SIZE_SUBTITLE};
        margin-top: -0.5rem;
        margin-bottom: 1.25rem;
    }}
    .empty-state {{
        border: 1px dashed {COLOR_BORDER_MUTED};
        border-radius: {RADIUS_EMPTY};
        padding: 2rem 1.5rem;
        text-align: center;
        color: {COLOR_TEXT_SUBTLE};
        background: {COLOR_BG_ELEVATED};
        margin: 1rem 0 1.5rem 0;
    }}
    .empty-state strong {{
        color: {COLOR_TEXT};
    }}
    div[data-testid="stMetric"] {{
        background: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: {RADIUS_CARD};
        padding: 0.75rem 1rem;
    }}
    .block-container {{
        padding-top: {SPACE_PAGE_TOP};
        max-width: {MAX_CONTENT_WIDTH};
    }}
    .legal-note {{
        color: {COLOR_TEXT_MUTED};
        font-size: {FONT_SIZE_LEGAL};
        border-top: 1px solid {COLOR_BORDER};
        padding-top: 1rem;
        margin-top: {SPACE_SECTION};
    }}
</style>
"""
