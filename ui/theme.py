"""SPEC-024: tema visual isolado."""

_DARK_CSS = """
<style>
    .stApp {
        background-color: #0f1419;
        color: #e7ecf1;
    }
    [data-testid="stSidebar"] {
        background-color: #151b23;
        border-right: 1px solid #243041;
    }
    [data-testid="stSidebar"] * {
        color: #e7ecf1;
    }
    h1, h2, h3 {
        color: #f3f6f9 !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }
    .main-subtitle {
        color: #8b9bb0;
        font-size: 0.95rem;
        margin-top: -0.5rem;
        margin-bottom: 1.25rem;
    }
    .empty-state {
        border: 1px dashed #2a3a4d;
        border-radius: 12px;
        padding: 2rem 1.5rem;
        text-align: center;
        color: #9aabbf;
        background: #121820;
        margin: 1rem 0 1.5rem 0;
    }
    .empty-state strong {
        color: #e7ecf1;
    }
    div[data-testid="stMetric"] {
        background: #151b23;
        border: 1px solid #243041;
        border-radius: 10px;
        padding: 0.75rem 1rem;
    }
    .block-container {
        padding-top: 1.5rem;
        max-width: 1100px;
    }
    .legal-note {
        color: #8b9bb0;
        font-size: 0.85rem;
        border-top: 1px solid #243041;
        padding-top: 1rem;
        margin-top: 2rem;
    }
</style>
"""


def dark_css() -> str:
    return _DARK_CSS
