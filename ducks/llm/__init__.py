"""Duck: provedores LLM pluggáveis."""

from ducks.llm.registry import (
    ProviderInfo,
    create_provider,
    default_model_for,
    get_enabled_providers,
    resolve_default_provider_id,
)

__all__ = [
    "ProviderInfo",
    "create_provider",
    "default_model_for",
    "get_enabled_providers",
    "resolve_default_provider_id",
]
