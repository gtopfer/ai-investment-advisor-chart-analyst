# Estado do Desenvolvimento (Task Tracker)

Este arquivo é lido e atualizado automaticamente pela IA para rastrear o status de cada especificação no diretório `.ai/specs/` e gerenciar a transição de fases.

## Como funciona
1. **Rastreamento Automático**: A IA verifica os arquivos na pasta `.ai/specs/` e atualiza a tabela abaixo com o status correspondente.
2. **Ciclo de Vida (Fases)**:
   - `draft` (Rascunho inicial do PM)
   - `spec_approved` (Requisitos de negócio aprovados pelo usuário; aguardando arquitetura)
   - `tech_approved` (Especificação técnica aprovada pelo usuário; aguardando testes)
   - `test_red` (Testes TDD escritos e falhando; aguardando implementação)
   - `code_review` (Implementado; passando por revisão estática)
   - `tested` (Testes passando com sucesso; aguardando validação do DoD pelo PM)
   - `done` (Entregue, documentado e concluído)

---

## Lista de Especificações Ativas

| Código | Título da Spec | Caminho do Arquivo | Status Atual | Próxima Fase | Última Atualização |
|--------|----------------|-------------------|--------------|--------------|---------------------|
| SPEC-005 | Suporte completo a criptoativos | `.ai/specs/005_crypto_support.md` | `done` | `done` | 2026-07-26 |
| SPEC-001 | Módulo multi-LLM (provedor configurável) | `.ai/specs/001_llm_provider_module.md` | `done` | `done` | 2026-07-26 |
| SPEC-002 | Layout amigável e minimalista | `.ai/specs/002_minimalist_layout.md` | `done` | `done` | 2026-07-26 |
| SPEC-003 | Importar carteira atual | `.ai/specs/003_import_current_portfolio.md` | `done` | `done` | 2026-07-26 |
| SPEC-004 | Visão “como deve ficar” (carteira projetada) | `.ai/specs/004_projected_portfolio_view.md` | `done` | `done` | 2026-07-26 |
| SPEC-000 | Configuração Inicial | `.ai/specs/000_setup.md` | `done` | `done` | 2026-07-18 |

---

## Histórico de Execuções Recentes

* **2026-07-26**: [SPEC-005] Aprovado e transicionado: `tested` ➔ `done` (Próxima Fase: `done`).
* **2026-07-26**: [SPEC-005] Aprovado e transicionado: `code_review` ➔ `tested` (Próxima Fase: `pm_dod`).
* **2026-07-26**: [SPEC-005] Aprovado e transicionado: `test_red` ➔ `code_review` (Próxima Fase: `qa_validation`).
* **2026-07-26**: [SPEC-005] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Próxima Fase: `developer`).
* **2026-07-26**: [SPEC-005] Aprovado e transicionado: `spec_approved` ➔ `tech_approved` (Próxima Fase: `qa_tdd`).
* **2026-07-26**: [SPEC-005] Aprovado e transicionado: `draft` ➔ `spec_approved` (Próxima Fase: `architect`).
* **2026-07-26**: SPEC-005 registrada em `draft` (PM). Suporte completo a cripto. Diagnóstico: score DY, normalização de ticker, labels R$/USD.
* **2026-07-26**: [SPEC-004] Aprovado e transicionado: `tested` ➔ `done` (Próxima Fase: `done`).
* **2026-07-26**: [SPEC-004] Aprovado e transicionado: `code_review` ➔ `tested` (Próxima Fase: `pm_dod`).
* **2026-07-26**: [SPEC-004] Aprovado e transicionado: `test_red` ➔ `code_review` (Próxima Fase: `qa_validation`).
* **2026-07-26**: [SPEC-004] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Próxima Fase: `developer`).
* **2026-07-26**: [SPEC-004] Aprovado e transicionado: `spec_approved` ➔ `tech_approved` (Próxima Fase: `qa_tdd`).
* **2026-07-26**: [SPEC-004] Aprovado e transicionado: `draft` ➔ `spec_approved` (Próxima Fase: `architect`).
* **2026-07-26**: [SPEC-003] Aprovado e transicionado: `tested` ➔ `done` (Próxima Fase: `done`).
* **2026-07-26**: [SPEC-003] Aprovado e transicionado: `code_review` ➔ `tested` (Próxima Fase: `pm_dod`).
* **2026-07-26**: [SPEC-003] Aprovado e transicionado: `test_red` ➔ `code_review` (Próxima Fase: `qa_validation`).
* **2026-07-26**: [SPEC-003] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Próxima Fase: `developer`).
* **2026-07-26**: [SPEC-003] Aprovado e transicionado: `spec_approved` ➔ `tech_approved` (Próxima Fase: `qa_tdd`).
* **2026-07-26**: [SPEC-003] Aprovado e transicionado: `draft` ➔ `spec_approved` (Próxima Fase: `architect`).
* **2026-07-26**: [SPEC-002] Aprovado e transicionado: `tested` ➔ `done` (Próxima Fase: `done`).
* **2026-07-26**: [SPEC-002] Aprovado e transicionado: `code_review` ➔ `tested` (Próxima Fase: `pm_dod`).
* **2026-07-26**: [SPEC-002] Aprovado e transicionado: `test_red` ➔ `code_review` (Próxima Fase: `qa_validation`).
* **2026-07-26**: [SPEC-002] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Próxima Fase: `developer`).
* **2026-07-26**: [SPEC-002] Aprovado e transicionado: `spec_approved` ➔ `tech_approved` (Próxima Fase: `qa_tdd`).
* **2026-07-26**: [SPEC-002] Aprovado e transicionado: `draft` ➔ `spec_approved` (Próxima Fase: `architect`).
* **2026-07-26**: [SPEC-001] Aprovado e transicionado: `tested` ➔ `done` (Próxima Fase: `done`).
* **2026-07-26**: [SPEC-001] Aprovado e transicionado: `code_review` ➔ `tested` (Próxima Fase: `pm_dod`).
* **2026-07-26**: [SPEC-001] Aprovado e transicionado: `test_red` ➔ `code_review` (Próxima Fase: `qa_validation`).
* **2026-07-26**: [SPEC-001] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Próxima Fase: `developer`).
* **2026-07-26**: [SPEC-001] Aprovado e transicionado: `spec_approved` ➔ `tech_approved` (Próxima Fase: `qa_tdd`).
* **2026-07-26**: [SPEC-001] Aprovado e transicionado: `draft` ➔ `spec_approved` (Próxima Fase: `architect`).
* **2026-07-26**: SPEC-004 (PM): decisões fechadas — projeção Atual vs Projetado + aplicar opt-in na carteira; zerar como “Sair”; sem carteira atual ainda mostra alvo. Aguardando `./devkit approve` na fila.
* **2026-07-26**: SPEC-004 registrada em `draft` (PM). Feature: atualizar/visualizar carteira do usuário com recomendações (“como deve ficar”). Aguardando decisões.
* **2026-07-26**: SPEC-003 (PM): decisões fechadas — CSV+TXT, substituir tudo, modo da UI, modelo baixável. Aguardando `./devkit approve` na fila.
* **2026-07-26**: SPEC-003 registrada em `draft` (PM). Feature: importar carteira atual. Aguardando decisões de formato/UX.
* **2026-07-26**: SPEC-002 (PM): decisões fechadas — tema escuro, sidebar colapsável, empty state + cards, emojis mínimos. Aguardando aprovação → `./devkit approve` (após ou junto da fila).
* **2026-07-26**: SPEC-002 registrada em `draft` (PM). Feature: layout amigável, limpo e minimalista. Aguardando decisões de UX.
* **2026-07-26**: SPEC-001 (PM): decisões fechadas — MVP Groq + OpenAI-compatible; env + seletor sidebar; modelo editável. Aguardando aprovação humana → `./devkit approve`.
* **2026-07-26**: SPEC-001 registrada em `draft` (PM). Feature: módulo para o usuário escolher/configurar qualquer LLM preferido.
* **2026-07-18**: Inicialização do repositório devkit-ai.
