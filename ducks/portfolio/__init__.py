"""Duck: carteira, alocação, rebalance, import/export e preferências."""

from ducks.portfolio.alerts import evaluate_alerts
from ducks.portfolio.allocator import (
    allocate_capital,
    build_projected_portfolio,
    build_rebalance_actions,
    compare_strategies,
    projected_positions_for_session,
    score_assets,
)
from ducks.portfolio.candidates import (
    build_candidate_tickers,
    classify_ticker,
    parse_extra_tickers,
)
from ducks.portfolio.export_csv import portfolio_target_to_csv, rebalance_actions_to_csv
from ducks.portfolio.import_portfolio import (
    PORTFOLIO_CSV_TEMPLATE,
    ImportResult,
    format_positions_as_text,
    import_portfolio_file,
    parse_current_portfolio,
    parse_portfolio_csv,
)
from ducks.portfolio.persistence import (
    DEFAULT_PREFS,
    QUERY_KEY,
    decode_prefs,
    encode_prefs,
    save_prefs_file,
)

__all__ = [
    "DEFAULT_PREFS",
    "PORTFOLIO_CSV_TEMPLATE",
    "QUERY_KEY",
    "ImportResult",
    "allocate_capital",
    "build_candidate_tickers",
    "build_projected_portfolio",
    "build_rebalance_actions",
    "classify_ticker",
    "compare_strategies",
    "decode_prefs",
    "encode_prefs",
    "evaluate_alerts",
    "format_positions_as_text",
    "import_portfolio_file",
    "parse_current_portfolio",
    "parse_extra_tickers",
    "parse_portfolio_csv",
    "portfolio_target_to_csv",
    "projected_positions_for_session",
    "rebalance_actions_to_csv",
    "save_prefs_file",
    "score_assets",
]
