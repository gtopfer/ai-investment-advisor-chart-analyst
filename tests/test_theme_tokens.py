"""Design system: tokens monocromáticos e CSS gerado."""

from ducks.ui.theme import (
    COLOR_BG,
    COLOR_BORDER,
    COLOR_SURFACE,
    COLOR_TEXT,
    TOKENS,
    dark_css,
)


def test_tokens_include_core_palette():
    assert TOKENS["color.bg"] == "#0f1419"
    assert TOKENS["color.surface"] == "#151b23"
    assert TOKENS["color.border"] == "#243041"
    assert TOKENS["color.text"] == "#e7ecf1"
    assert COLOR_BG == TOKENS["color.bg"]
    assert COLOR_SURFACE == TOKENS["color.surface"]
    assert COLOR_BORDER == TOKENS["color.border"]
    assert COLOR_TEXT == TOKENS["color.text"]


def test_dark_css_uses_named_tokens_not_orphaned_hex():
    css = dark_css()
    assert COLOR_BG in css
    assert COLOR_SURFACE in css
    assert COLOR_TEXT in css
    assert ".empty-state" in css
    assert ".legal-note" in css
    assert "<style>" in css


def test_palette_is_monochrome_hex_shape():
    """Todos os tokens de cor são hex de 7 chars (#rrggbb)."""
    for key, value in TOKENS.items():
        if not key.startswith("color."):
            continue
        assert value.startswith("#") and len(value) == 7, f"{key}={value}"
