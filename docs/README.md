# Documentação

Índice da documentação deste projeto.

## Por onde começar

- Processo de agentes (**jojo-ai**): [`agents.md`](../agents.md), [`system-design.md`](../system-design.md), [`CHANGELOG.md`](../CHANGELOG.md) na raiz; kit em [`kit/`](../kit/)
- [`CHANGELOG.md`](CHANGELOG.md) — histórico de mudanças notáveis do produto
- [`BACKLOG.md`](BACKLOG.md) — melhorias futuras SPEC-016…035
- Spec técnica detalhada: [`technical-spec.md`](technical-spec.md)
- Requisitos de produto (legado PM): [`product-requirements.md`](product-requirements.md)
- Cenários BDD: [`features.feature`](features.feature)
- Specs por feature: [`specs/`](specs/)

## Histórico de Features

- [SPEC-001 — Módulo multi-LLM](specs/001_llm_provider_module.md) (`done`)
- [SPEC-002 — Layout minimalista](specs/002_minimalist_layout.md) (`done`)
- [SPEC-003 — Importar carteira](specs/003_import_current_portfolio.md) (`done`)
- [SPEC-004 — Como deve ficar](specs/004_projected_portfolio_view.md) (`done`)
- [SPEC-005 — Suporte a cripto](specs/005_crypto_support.md) (`done`)
- [SPEC-006 — HOTFIX harness review](specs/006_harness_devkit_review_estável_pytest_path_ruff.md) (`done`)
- [SPEC-007 — Unificar parse de carteira](specs/007_unificar_parse_de_carteira_app_portfolio.md) (`done`)
- [SPEC-008 — Remover BDRs do multiselect](specs/008_classe_bdrs_remover_opção_morta_ou_suportar_universo.md) (`done`)
- [SPEC-009 — Remover plotly](specs/009_remover_dependência_plotly_não_utilizada.md) (`done`)
- [SPEC-010 — Avisos de histórico curto](specs/010_avisos_de_qualidade_de_dados_histórico_curto_indicadores_neutros.md) (`done`)
- [SPEC-011 — Extrair domínio + logging](specs/011_extrair_núcleo_de_domínio_de_apppy_logging_estruturado.md) (`done`)
- [SPEC-012 — Export CSV carteira/rebalance](specs/012_exportar_carteira_e_plano_de_rebalanceamento.md) (`done`)
- [SPEC-013 — Persistir preferências no browser](specs/013_persistir_carteira_e_preferências_entre_sessões.md) (`done`)
- [SPEC-014 — Suporte a BDRs](specs/014_suporte_completo_a_bdrs_como_classe_de_ativos.md) (`done`)
- [SPEC-015 — Threshold de rebalance](specs/015_threshold_de_rebalanceamento_por_desvio_percentual.md) (`done`)

Backlog (016–035): ver [BACKLOG.md](BACKLOG.md).

## Processo (jojo-ai v1.4)

| Arquivo | Função |
| --- | --- |
| `agents.md` | Produto + **`### Features`** (backlog humano) + fluxo |
| `system-design.md` | Arquitetura + design system |
| `CHANGELOG.md` (raiz) | Feito vs pendente (trabalho ativo) |
| `kit/` | Runbooks, skills, scripts, templates |

**Nova feature:** edite `agents.md` → Seção 1 → `### Features` com um item `- [ ] …` e diga à IA: *siga agents.md*.