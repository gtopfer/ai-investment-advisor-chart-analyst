# Instruções para o Gemini CLI

## REGRA ABSOLUTA (CICLO DE VIDA & ESTADO)
Toda mudança de código ou documentação é governada por especificações localizadas no diretório [`.ai/specs/`](.ai/specs/) e gerenciada pelo arquivo de controle de progresso [`.ai/state.md`](.ai/state.md).

Ao iniciar qualquer interação neste repositório:
1. **Leia obrigatoriamente** as instruções completas em [`.ai/global.instructions`](.ai/global.instructions).
2. **Execute a Rotina de Inicialização**:
   - Sincronize `.ai/specs/` e [`.ai/state.md`](.ai/state.md).
   - Identifique a especificação ativa.
   - Chame o orquestrador em [`.ai/agents/squad-lead.agent.md`](.ai/agents/squad-lead.agent.md) para conduzir o desenvolvimento com base no status atual (PM -> Architect -> QA/TDD -> Developer -> QA/Validação -> PM/DoD).
