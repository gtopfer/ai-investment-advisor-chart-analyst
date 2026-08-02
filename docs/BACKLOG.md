# Backlog de melhorias (SPEC-016 … SPEC-035)

Registrado em **2026-08-01** a partir da auditoria de produto/engenharia.  
Todas as specs estão em `.ai/specs/` com status **`draft` (PM)** no `.ai/state.md`.

Ordem sugerida de execução (respeita dependências):

## Onda A — Credibilidade e utilidade (P0)

| Spec | Título | Depende de |
|------|--------|------------|
| [SPEC-016](../.ai/specs/016_moeda_base_e_conversão_cambial_honesta.md) | Moeda-base e conversão cambial | — |
| [SPEC-017](../.ai/specs/017_tickers_extras_e_universo_expansível.md) | Tickers extras / universo | — |
| [SPEC-019](../.ai/specs/019_transparência_e_calibragem_do_score.md) | Transparência do score | — |
| [SPEC-018](../.ai/specs/018_performance_e_modo_rápido_de_geração.md) | Performance e modo rápido | 017 (ideal) |

## Onda B — UX de decisão (P1)

| Spec | Título | Depende de |
|------|--------|------------|
| [SPEC-023](../.ai/specs/023_onboarding_dx_dotenv_readme_e_empty_ctas.md) | dotenv, README, empty CTAs | — |
| [SPEC-021](../.ai/specs/021_histórico_de_runs_na_sessão.md) | Histórico de runs | — |
| [SPEC-022](../.ai/specs/022_persistência_robusta_de_preferências.md) | Persistência robusta | 013 done; melhora 013 |
| [SPEC-020](../.ai/specs/020_comparar_estratégias_lado_a_lado.md) | Comparar estratégias | 018, 019 |

## Onda C — Engenharia (P2)

| Spec | Título | Depende de |
|------|--------|------------|
| [SPEC-024](../.ai/specs/024_fatiar_ui_em_módulos_sidebar_results_theme.md) | Fatiar UI | — |
| [SPEC-025](../.ai/specs/025_data_fetcher_desacoplado_do_cache_streamlit.md) | Fetcher sem st.cache | — |
| [SPEC-027](../.ai/specs/027_observabilidade_de_runs_logging_estruturado.md) | Logging estruturado | 018 (ideal) |
| [SPEC-026](../.ai/specs/026_mypy_gradual_e_teste_de_integração_do_pipeline.md) | mypy + integração | 025 |

## Onda D — Produto avançado (P3)

| Spec | Título | Depende de |
|------|--------|------------|
| [SPEC-032](../.ai/specs/032_explicação_de_riscos_da_ia_e_disclaimer_reforçado.md) | Riscos IA / disclaimer | — |
| [SPEC-028](../.ai/specs/028_custos_de_corretagem_e_ir_simplificado_no_rebalance.md) | Custos corretagem/IR | 016 |
| [SPEC-029](../.ai/specs/029_metas_de_alocação_por_classe_de_ativo.md) | Metas por classe | 016, 019 |
| [SPEC-030](../.ai/specs/030_watchlist_e_alertas_técnicosdividendos.md) | Watchlist e alertas | 017, 022 |
| [SPEC-031](../.ai/specs/031_gráficos_de_preço_no_detalhe_do_ativo.md) | Gráficos de preço | 024, 025 |
| [SPEC-033](../.ai/specs/033_modo_offline_e_fixtures_de_mercado.md) | Offline / fixtures | 025 |
| [SPEC-034](../.ai/specs/034_docker_one_command_run.md) | Docker | 023 |
| [SPEC-035](../.ai/specs/035_i18n_inglês_da_interface.md) | i18n EN | 024 |

## Como puxar o trabalho

```bash
./devkit activate SPEC-016   # ou outra
# No chat: refinar PM → ./devkit approve → UX → Architect → …
```

Specs **sem UI de produto** (refactor/tooling): 024, 025, 026, 027, 034 — fase UX pode ser N/A rápido.

## Já entregue (contexto)

012–015 (export, threshold, BDRs, prefs URL), 006–011 (higiene), 001–005 (features base).
