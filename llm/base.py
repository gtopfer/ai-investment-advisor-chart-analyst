from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    """Contrato mínimo: completa um chat e devolve o texto da resposta."""

    provider_id: str
    display_name: str

    def complete_chat(self, system: str, user: str, model: str) -> str:
        """Retorna o conteúdo textual da mensagem do assistente."""
        ...
