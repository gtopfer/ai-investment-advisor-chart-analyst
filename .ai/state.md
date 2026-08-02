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
| SPEC-035 | i18n inglês da interface | `.ai/specs/035_i18n_inglês_da_interface.md` | `done` | `done` | 2026-08-01 |
| SPEC-034 | Docker one-command run | `.ai/specs/034_docker_one_command_run.md` | `done` | `done` | 2026-08-01 |
| SPEC-033 | Modo offline e fixtures de mercado | `.ai/specs/033_modo_offline_e_fixtures_de_mercado.md` | `done` | `done` | 2026-08-01 |
| SPEC-032 | Explicação de riscos da IA e disclaimer reforçado | `.ai/specs/032_explicação_de_riscos_da_ia_e_disclaimer_reforçado.md` | `done` | `done` | 2026-08-01 |
| SPEC-031 | Gráficos de preço no detalhe do ativo | `.ai/specs/031_gráficos_de_preço_no_detalhe_do_ativo.md` | `done` | `done` | 2026-08-01 |
| SPEC-030 | Watchlist e alertas técnicos/dividendos | `.ai/specs/030_watchlist_e_alertas_técnicosdividendos.md` | `done` | `done` | 2026-08-01 |
| SPEC-029 | Metas de alocação por classe de ativo | `.ai/specs/029_metas_de_alocação_por_classe_de_ativo.md` | `done` | `done` | 2026-08-01 |
| SPEC-028 | Custos de corretagem e IR simplificado no rebalance | `.ai/specs/028_custos_de_corretagem_e_ir_simplificado_no_rebalance.md` | `done` | `done` | 2026-08-01 |
| SPEC-027 | Observabilidade de runs (logging estruturado) | `.ai/specs/027_observabilidade_de_runs_logging_estruturado.md` | `done` | `done` | 2026-08-01 |
| SPEC-026 | Mypy gradual e teste de integração do pipeline | `.ai/specs/026_mypy_gradual_e_teste_de_integração_do_pipeline.md` | `done` | `done` | 2026-08-01 |
| SPEC-025 | Data fetcher desacoplado do cache Streamlit | `.ai/specs/025_data_fetcher_desacoplado_do_cache_streamlit.md` | `done` | `done` | 2026-08-01 |
| SPEC-024 | Fatiar UI em módulos (sidebar, results, theme) | `.ai/specs/024_fatiar_ui_em_módulos_sidebar_results_theme.md` | `done` | `done` | 2026-08-01 |
| SPEC-023 | Onboarding DX: dotenv, README e empty CTAs | `.ai/specs/023_onboarding_dx_dotenv_readme_e_empty_ctas.md` | `done` | `done` | 2026-08-01 |
| SPEC-022 | Persistência robusta de preferências | `.ai/specs/022_persistência_robusta_de_preferências.md` | `done` | `done` | 2026-08-01 |
| SPEC-021 | Histórico de runs na sessão | `.ai/specs/021_histórico_de_runs_na_sessão.md` | `done` | `done` | 2026-08-01 |
| SPEC-020 | Comparar estratégias lado a lado | `.ai/specs/020_comparar_estratégias_lado_a_lado.md` | `done` | `done` | 2026-08-01 |
| SPEC-019 | Transparência e calibragem do score | `.ai/specs/019_transparência_e_calibragem_do_score.md` | `done` | `done` | 2026-08-01 |
| SPEC-018 | Performance e modo rápido de geração | `.ai/specs/018_performance_e_modo_rápido_de_geração.md` | `done` | `done` | 2026-08-01 |
| SPEC-017 | Tickers extras e universo expansível | `.ai/specs/017_tickers_extras_e_universo_expansível.md` | `done` | `done` | 2026-08-01 |
| SPEC-016 | Moeda-base e conversão cambial honesta | `.ai/specs/016_moeda_base_e_conversão_cambial_honesta.md` | `done` | `done` | 2026-08-01 |
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

* **2026-08-01**: [SPEC-035] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-035] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-035] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-035] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-035] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-035] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-035] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-035] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-034] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-034] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-034] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-034] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-034] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-034] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-034] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-034] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-033] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-033] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-033] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-033] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-033] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-033] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-033] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-033] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-032] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-032] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-032] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-032] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-032] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-032] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-032] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-032] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-031] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-031] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-031] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-031] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-031] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-031] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-031] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-031] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-030] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-030] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-030] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-030] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-030] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-030] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-030] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-030] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-029] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-029] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-029] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-029] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-029] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-029] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-029] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-029] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-028] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-028] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-028] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-028] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-028] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-028] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-028] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-028] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-027] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-027] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-027] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-027] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-027] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-027] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-027] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-027] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-026] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-026] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-026] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-026] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-026] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-026] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-026] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-026] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-025] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-025] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-025] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-025] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-025] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-025] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-025] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-025] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-024] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-024] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-024] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-024] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-024] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-024] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-024] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-024] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-023] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-023] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-023] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-023] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-023] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-023] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-023] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-023] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-022] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-022] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-022] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-022] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-022] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-022] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-022] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-022] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-021] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-021] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-021] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-021] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-021] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-021] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-021] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-021] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-020] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-020] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-020] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-020] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-020] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-020] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-020] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-020] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-019] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-019] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-019] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-019] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-019] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-019] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-019] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-019] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-018] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-018] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-018] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-018] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-018] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-018] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-018] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-018] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-017] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-017] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-017] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-017] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-017] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-017] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-017] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-017] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-016] Aprovado e transicionado: `tested` ➔ `done` (Fase Ativa: `done`).
* **2026-08-01**: [SPEC-016] Aprovado e transicionado: `code_review` ➔ `tested` (Fase Ativa: `pm_dod`).
* **2026-08-01**: [SPEC-016] Aprovado e transicionado: `test_red` ➔ `code_review` (Fase Ativa: `qa_validation`).
* **2026-08-01**: [SPEC-016] Aprovado e transicionado: `tech_approved` ➔ `test_red` (Fase Ativa: `developer`).
* **2026-08-01**: [SPEC-016] Aprovado e transicionado: `ux_approved` ➔ `tech_approved` (Fase Ativa: `qa_tdd`).
* **2026-08-01**: [SPEC-016] Aprovado e transicionado: `spec_approved` ➔ `ux_approved` (Fase Ativa: `architect`).
* **2026-08-01**: [SPEC-016] Aprovado e transicionado: `draft` ➔ `spec_approved` (Fase Ativa: `ux`).
* **2026-08-01**: [SPEC-016] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: [SPEC-016] ativada como spec prioritária (topo da fila ativa).
* **2026-08-01**: Nova especificação `SPEC-035` (`035_i18n_inglês_da_interface.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-034` (`034_docker_one_command_run.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-033` (`033_modo_offline_e_fixtures_de_mercado.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-032` (`032_explicação_de_riscos_da_ia_e_disclaimer_reforçado.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-031` (`031_gráficos_de_preço_no_detalhe_do_ativo.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-030` (`030_watchlist_e_alertas_técnicosdividendos.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-029` (`029_metas_de_alocação_por_classe_de_ativo.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-028` (`028_custos_de_corretagem_e_ir_simplificado_no_rebalance.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-027` (`027_observabilidade_de_runs_logging_estruturado.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-026` (`026_mypy_gradual_e_teste_de_integração_do_pipeline.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-025` (`025_data_fetcher_desacoplado_do_cache_streamlit.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-024` (`024_fatiar_ui_em_módulos_sidebar_results_theme.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-023` (`023_onboarding_dx_dotenv_readme_e_empty_ctas.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-022` (`022_persistência_robusta_de_preferências.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-021` (`021_histórico_de_runs_na_sessão.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-020` (`020_comparar_estratégias_lado_a_lado.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-019` (`019_transparência_e_calibragem_do_score.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-018` (`018_performance_e_modo_rápido_de_geração.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-017` (`017_tickers_extras_e_universo_expansível.md`) status `draft` fase `pm`.
* **2026-08-01**: Nova especificação `SPEC-016` (`016_moeda_base_e_conversão_cambial_honesta.md`) status `draft` fase `pm`.
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
