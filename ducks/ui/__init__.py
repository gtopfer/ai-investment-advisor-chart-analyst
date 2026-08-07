"""Duck: interface Streamlit (layout, theme, i18n)."""

from ducks.ui.layout import (
    display_portfolio,
    display_projected_portfolio,
    display_rebalance_plan,
    display_strategy_comparison,
    display_summary_metrics,
    display_watchlist_alerts,
    render_disclaimer,
    render_empty_state,
    render_header,
    render_sidebar,
)
from ducks.ui.theme import dark_css

__all__ = [
    "dark_css",
    "display_portfolio",
    "display_projected_portfolio",
    "display_rebalance_plan",
    "display_strategy_comparison",
    "display_summary_metrics",
    "display_watchlist_alerts",
    "render_disclaimer",
    "render_empty_state",
    "render_header",
    "render_sidebar",
]
