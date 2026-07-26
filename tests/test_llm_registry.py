from llm import registry


def test_get_enabled_providers_groq_only(monkeypatch):
    monkeypatch.setattr(registry, "GROQ_API_KEY", "gsk-test")
    monkeypatch.setattr(registry, "OPENAI_BASE_URL", "")
    monkeypatch.setattr(registry, "OPENAI_API_KEY", "")
    monkeypatch.setattr(registry, "LLM_PROVIDER", "")

    enabled = registry.get_enabled_providers()
    assert len(enabled) == 1
    assert enabled[0].provider_id == "groq"
    assert registry.resolve_default_provider_id(enabled) == "groq"


def test_get_enabled_providers_openai_compatible_localhost(monkeypatch):
    monkeypatch.setattr(registry, "GROQ_API_KEY", "")
    monkeypatch.setattr(registry, "OPENAI_BASE_URL", "http://localhost:11434/v1")
    monkeypatch.setattr(registry, "OPENAI_API_KEY", "")
    monkeypatch.setattr(registry, "OPENAI_MODEL", "llama3")
    monkeypatch.setattr(registry, "LLM_PROVIDER", "")

    enabled = registry.get_enabled_providers()
    assert any(p.provider_id == "openai_compatible" for p in enabled)
    assert registry.resolve_default_provider_id(enabled) == "openai_compatible"


def test_resolve_prefers_llm_provider_env(monkeypatch):
    monkeypatch.setattr(registry, "GROQ_API_KEY", "gsk-test")
    monkeypatch.setattr(registry, "OPENAI_BASE_URL", "https://api.openai.com/v1")
    monkeypatch.setattr(registry, "OPENAI_API_KEY", "sk-test")
    monkeypatch.setattr(registry, "LLM_PROVIDER", "openai_compatible")

    enabled = registry.get_enabled_providers()
    assert registry.resolve_default_provider_id(enabled) == "openai_compatible"


def test_create_provider_unknown_raises(monkeypatch):
    monkeypatch.setattr(registry, "GROQ_API_KEY", "gsk-test")
    try:
        registry.create_provider("unknown")
        assert False, "should raise"
    except ValueError as exc:
        assert "desconhecido" in str(exc).lower()
