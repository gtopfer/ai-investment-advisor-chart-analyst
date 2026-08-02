# Documentação

Índice da documentação deste projeto.

## Por onde começar
- [`CHANGELOG.md`](CHANGELOG.md) — histórico de mudanças notáveis, mais recente primeiro
- As duas specs do projeto vivem em [`.ai/`](../.ai/), na raiz: [`template.specs`](../.ai/template.specs) (requisito do app, do PM) e [`technical-spec.md`](../.ai/technical-spec.md) (especificação técnica de construção, do Architect — inclui o histórico de decisões arquiteturais)
- Cenários BDD ficam em [`.ai/features.feature`](../.ai/features.feature)
- Specs de API, guias de deploy e documentação de schema de banco de dados vão direto nesta pasta, conforme forem escritos

## Histórico de Features
- [SPEC-001 — Módulo multi-LLM](../.ai/specs/001_llm_provider_module.md) (`done`)
- [SPEC-002 — Layout minimalista](../.ai/specs/002_minimalist_layout.md) (`done`)
- [SPEC-003 — Importar carteira](../.ai/specs/003_import_current_portfolio.md) (`done`)
- [SPEC-004 — Como deve ficar](../.ai/specs/004_projected_portfolio_view.md) (`done`)
- [SPEC-005 — Suporte a cripto](../.ai/specs/005_crypto_support.md) (`done`)
- [SPEC-006 — HOTFIX harness review](../.ai/specs/006_harness_devkit_review_estável_pytest_path_ruff.md) (`done`)
- [SPEC-007 — Unificar parse de carteira](../.ai/specs/007_unificar_parse_de_carteira_app_portfolio.md) (`done`)
- [SPEC-008 — Remover BDRs do multiselect](../.ai/specs/008_classe_bdrs_remover_opção_morta_ou_suportar_universo.md) (`done`)
- [SPEC-009 — Remover plotly](../.ai/specs/009_remover_dependência_plotly_não_utilizada.md) (`done`)
- [SPEC-010 — Avisos de histórico curto](../.ai/specs/010_avisos_de_qualidade_de_dados_histórico_curto_indicadores_neutros.md) (`done`)
- [SPEC-011 — Extrair domínio + logging](../.ai/specs/011_extrair_núcleo_de_domínio_de_apppy_logging_estruturado.md) (`done`)
- [SPEC-012 — Export CSV carteira/rebalance](../.ai/specs/012_exportar_carteira_e_plano_de_rebalanceamento.md) (`done`)
- [SPEC-013 — Persistir preferências no browser](../.ai/specs/013_persistir_carteira_e_preferências_entre_sessões.md) (`done`)
- [SPEC-014 — Suporte a BDRs](../.ai/specs/014_suporte_completo_a_bdrs_como_classe_de_ativos.md) (`done`)
- [SPEC-015 — Threshold de rebalance](../.ai/specs/015_threshold_de_rebalanceamento_por_desvio_percentual.md) (`done`)

## DevKit
- [Guia do Usuário do DevKit](GUIA-DO-USUARIO.md) — ciclo de vida, CLI e fases (inclui UX)
