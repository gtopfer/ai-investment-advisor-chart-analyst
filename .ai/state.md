# Estado do Desenvolvimento (Task Tracker)

Este arquivo é lido e atualizado automaticamente pela IA para rastrear o status de cada especificação no diretório `.ai/specs/` e gerenciar a transição de fases.

## Como funciona
1. **Rastreamento Automático**: A IA verifica os arquivos na pasta `.ai/specs/` e atualiza a tabela abaixo com o status correspondente.
2. **Ciclo de Vida (Fases)** — DevKit-AI atualizado em 2026-07-26:
   - `draft` (Rascunho inicial do PM)
   - `spec_approved` (Requisitos de negócio aprovados; aguardando UI/UX)
   - `ux_approved` (UI/UX aprovada; aguardando arquitetura técnica)
   - `tech_approved` (Especificação técnica aprovada; aguardando testes TDD)
   - `test_red` (Testes TDD escritos e falhando; aguardando implementação)
   - `code_review` (Implementado; validação de QA)
   - `tested` (Testes ok; validação de DoD do PM)
   - `done` (Entregue, documentado e concluído)

---

## Lista de Especificações Ativas

| Código | Título da Spec | Caminho do Arquivo | Status Atual | Fase Ativa | Última Atualização |
|--------|----------------|-------------------|--------------|------------|---------------------|
| SPEC-013 | Persistir carteira e preferências entre sessões | `.ai/specs/013_persistir_carteira_e_preferências_entre_sessões.md` | `done` | `done` | 2026-08-01 |
| SPEC-014 | Suporte completo a BDRs como classe de ativos | `.ai/specs/014_suporte_completo_a_bdrs_como_classe_de_ativos.md` | `done` | `done` | 2026-08-01 |
| SPEC-015 | Threshold de rebalanceamento por desvio percentual | `.ai/specs/015_threshold_de_rebalanceamento_por_desvio_percentual.md` | `done` | `done` | 2026-08-01 |
| SPEC-012 | Exportar carteira e plano de rebalanceamento | `.ai/specs/012_exportar_carteira_e_plano_de_rebalanceamento.md` | `done` | `done` | 2026-08-01 |
| SPEC-011 | Extrair núcleo de domínio de app.py + logging estruturado | `.ai/specs/011_extrair_núcleo_de_domínio_de_apppy_logging_estruturado.md` | `done` | `done` | 2026-07-26 |
| SPEC-010 | Avisos de qualidade de dados (histórico curto / indicadores neutros) | `.ai/specs/010_avisos_de_qualidade_de_dados_histórico_curto_indicadores_neutros.md` | `done` | `done` | 2026-07-26 |
| SPEC-009 | Remover dependência plotly não utilizada | `.ai/specs/009_remover_dependência_plotly_não_utilizada.md` | `done` | `done` | 2026-07-26 |
| SPEC-008 | Classe BDRs: remover opção morta ou suportar universo | `.ai/specs/008_classe_bdrs_remover_opção_morta_ou_suportar_universo.md` | `done` | `done` | 2026-07-26 |
| SPEC-007 | Unificar parse de carteira (app + portfolio) | `.ai/specs/007_unificar_parse_de_carteira_app_portfolio.md` | `done` | `done` | 2026-07-26 |
| SPEC-006 | [HOTFIX] Harness ./devkit review estável (pytest path + ruff) | `.ai/specs/006_harness_devkit_review_estável_pytest_path_ruff.md` | `done` | `done` | 2026-07-26 |
| SPEC-005 | Suporte completo a criptoativos | `.ai/specs/005_crypto_support.md` | `done` | `done` | 2026-07-26 |
| SPEC-001 | Módulo multi-LLM (provedor configurável) | `.ai/specs/001_llm_provider_module.md` | `done` | `done` | 2026-07-26 |
| SPEC-002 | Layout amigável e minimalista | `.ai/specs/002_minimalist_layout.md` | `done` | `done` | 2026-07-26 |
| SPEC-003 | Importar carteira atual | `.ai/specs/003_import_current_portfolio.md` | `done` | `done` | 2026-07-26 |
| SPEC-004 | Visão “como deve ficar” (carteira projetada) | `.ai/specs/004_projected_portfolio_view.md` | `done` | `done` | 2026-07-26 |
| SPEC-000 | Configuração Inicial | `.ai/specs/000_setup.md` | `done` | `done` | 2026-07-18 |

---

## Histórico de Execuções Recentes

* **2026-08-01**: [SPEC-013] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-013] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-013] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-013] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-013] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-013] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-013] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-013] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-014] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-014] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-014] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-014] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-014] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-014] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-014] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-014] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-015] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-015] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-015] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-015] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-015] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-015] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-015] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-015] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-012] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-012] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-012] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-012] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-012] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-012] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-012] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-012] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-012] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-012] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: Nova especificação `SPEC-015` (`015_threshold_de_rebalanceamento_por_desvio_percentual.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-014` (`014_suporte_completo_a_bdrs_como_classe_de_ativos.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-013` (`013_persistir_carteira_e_preferências_entre_sessões.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-012` (`012_exportar_carteira_e_plano_de_rebalanceamento.md`) status `draft` fase `pm`.
* **2026-07-26**: [SPEC-011] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-07-26**: [SPEC-011] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-07-26**: [SPEC-011] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-07-26**: [SPEC-011] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-07-26**: [SPEC-011] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-07-26**: [SPEC-011] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-07-26**: [SPEC-011] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-07-26**: [SPEC-011] ativada como spec prioritária (topo da fila ativa).
* **2026-07-26**: [SPEC-010] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-07-26**: [SPEC-010] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-07-26**: [SPEC-010] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-07-26**: [SPEC-010] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-07-26**: [SPEC-010] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-07-26**: [SPEC-010] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-07-26**: [SPEC-010] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-07-26**: [SPEC-010] ativada como spec prioritária (topo da fila ativa).
* **2026-07-26**: [SPEC-009] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-07-26**: [SPEC-009] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-07-26**: [SPEC-009] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-07-26**: [SPEC-009] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-07-26**: [SPEC-009] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-07-26**: [SPEC-009] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-07-26**: [SPEC-009] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-07-26**: [SPEC-009] ativada como spec prioritária (topo da fila ativa).
* **2026-07-26**: [SPEC-008] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-07-26**: [SPEC-008] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-07-26**: [SPEC-008] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-07-26**: [SPEC-008] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-07-26**: [SPEC-008] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-07-26**: [SPEC-008] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-07-26**: [SPEC-008] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-07-26**: [SPEC-008] ativada como spec prioritária (topo da fila ativa).
* **2026-07-26**: [SPEC-007] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-07-26**: [SPEC-007] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-07-26**: [SPEC-007] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-07-26**: [SPEC-007] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-07-26**: [SPEC-007] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-07-26**: [SPEC-007] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-07-26**: [SPEC-007] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-07-26**: [SPEC-007] ativada como spec prioritária (topo da fila ativa).
* **2026-07-26**: [SPEC-006] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-07-26**: [SPEC-006] ativada como spec prioritária (topo da fila ativa).
* **2026-07-26**: [SPEC-006] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-07-26**: [SPEC-006] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-07-26**: [SPEC-006] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-07-26**: [SPEC-006] ativada como spec prioritária (topo da fila ativa).
* **2026-07-26**: [SPEC-008] ativada como spec prioritária (topo da fila ativa).
* **2026-07-26**: [SPEC-006] ativada como spec prioritária (topo da fila ativa).
* **2026-07-26**: Nova especificação `SPEC-011` (`011_extrair_núcleo_de_domínio_de_apppy_logging_estruturado.md`) status `draft` fase `pm`.
* **2026-07-26**: Nova especificação `SPEC-010` (`010_avisos_de_qualidade_de_dados_histórico_curto_indicadores_neutros.md`) status `draft` fase `pm`.
* **2026-07-26**: Nova especificação `SPEC-009` (`009_remover_dependência_plotly_não_utilizada.md`) status `draft` fase `pm`.
* **2026-07-26**: Nova especificação `SPEC-008` (`008_classe_bdrs_remover_opção_morta_ou_suportar_universo.md`) status `draft` fase `pm`.
* **2026-07-26**: Nova especificação `SPEC-007` (`007_unificar_parse_de_carteira_app_portfolio.md`) status `draft` fase `pm`.
* **2026-07-26**: Nova especificação `SPEC-006` (`006_harness_devkit_review_estável_pytest_path_ruff.md`) status `tech_approved` fase `qa_tdd`.
* **2026-07-26**: DevKit-AI atualizado a partir de `devkit-ai` (commit de maturidade): CLI expandida (`doctor`, `log`, `activate`, `hotfix`, `reject`, `sync --migrate-lifecycle`), fase UX (`ux_approved` + agent `ux-designer` + skills `ui-ux`/`microcopy`), templates ADR/tech-spec, hooks, CI `devkit-review`, `docs/GUIA-DO-USUARIO.md`. Specs/state/tech-spec/guidelines de produto preservados. `./devkit doctor` APROVADO.
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
