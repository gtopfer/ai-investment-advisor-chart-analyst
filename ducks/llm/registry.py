from dataclasses import dataclass

from ducks.llm.base import LLMProvider
from ducks.llm.groq_provider import GroqProvider
from ducks.llm.openai_compatible import OpenAICompatibleProvider
from shared.config.config import (
    GROQ_API_KEY,
    GROQ_MODEL_NAME,
    LLM_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
)


@dataclass(frozen=True)
class ProviderInfo:
    provider_id: str
    display_name: str
    default_model: str
    credentials_ok: bool


def _groq_enabled() -> bool:
    return bool(GROQ_API_KEY.strip())


def _openai_compatible_enabled() -> bool:
    # base_url local (Ollama) pode funcionar com key vazia; exige base_url configurada
    return bool(OPENAI_BASE_URL.strip()) and (
        bool(OPENAI_API_KEY.strip()) or "localhost" in OPENAI_BASE_URL or "127.0.0.1" in OPENAI_BASE_URL
    )


def get_enabled_providers() -> list[ProviderInfo]:
    providers: list[ProviderInfo] = []
    if _groq_enabled():
        providers.append(
            ProviderInfo(
                provider_id="groq",
                display_name="Groq",
                default_model=GROQ_MODEL_NAME,
                credentials_ok=True,
            )
        )
    if _openai_compatible_enabled():
        providers.append(
            ProviderInfo(
                provider_id="openai_compatible",
                display_name="OpenAI-compatible",
                default_model=OPENAI_MODEL,
                credentials_ok=True,
            )
        )
    return providers


def resolve_default_provider_id(enabled: list[ProviderInfo] | None = None) -> str | None:
    providers = enabled if enabled is not None else get_enabled_providers()
    if not providers:
        return None
    ids = {p.provider_id for p in providers}
    preferred = (LLM_PROVIDER or "").strip().lower()
    if preferred in ids:
        return preferred
    if "groq" in ids:
        return "groq"
    return providers[0].provider_id


def default_model_for(provider_id: str) -> str:
    if provider_id == "groq":
        return GROQ_MODEL_NAME
    if provider_id == "openai_compatible":
        return OPENAI_MODEL
    return GROQ_MODEL_NAME


def create_provider(provider_id: str) -> LLMProvider:
    if provider_id == "groq":
        if not _groq_enabled():
            raise ValueError("Provedor Groq sem GROQ_API_KEY configurada.")
        return GroqProvider(api_key=GROQ_API_KEY)
    if provider_id == "openai_compatible":
        if not _openai_compatible_enabled():
            raise ValueError("Provedor OpenAI-compatible sem base_url/credenciais.")
        return OpenAICompatibleProvider(api_key=OPENAI_API_KEY or "ollama", base_url=OPENAI_BASE_URL)
    raise ValueError(f"Provedor desconhecido: {provider_id}")
