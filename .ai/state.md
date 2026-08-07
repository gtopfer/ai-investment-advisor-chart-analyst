# Estado (jojo run)

Atualizado: 2026-08-07T16:40:34Z

**Próxima feature:** — (nenhuma pendente)

## Pendentes

- (vazio)

## Feitas

- [x] Design system minimalista monocromático — `docs/design-system.md` + tokens em `ducks/ui/theme.py` + §3 `system-design.md`
- [x] Refatoração Ducks Pattern — `ducks/{market,analysis,portfolio,llm,ui}` + `shared/{config,models,utils}`; APIs públicas; `system-design.md` §2 atualizado
- [x] Multi-LLM (Groq + OpenAI-compatible) — `ducks/llm/` + registry + testes
- [x] Layout minimalista escuro — `ducks/ui/theme.py`, `layout.py`
- [x] Importar carteira atual via CSV/TXT + modelo baixável — `ducks/portfolio/import_portfolio.py`
- [x] Visão “Como deve ficar” (projetada) e aplicar na sessão — `build_projected_portfolio`
- [x] Suporte a cripto (normalização -USD, score só técnico) — testes crypto
- [x] Harness de testes/lint estável (pytest path + ruff) — `pytest.ini`, `ruff.toml`
- [x] Parse de carteira unificado em `ducks/portfolio/`
- [x] Remover BDRs mortos do multiselect → depois BDRs reais (SPEC-008 + SPEC-014)
- [x] Remover dependência plotly não usada — ausente de `requirements.txt`
- [x] Avisos de qualidade de dados (histórico curto) — `insufficient_history`
- [x] Extrair núcleo de domínio de `app.py` + logging — `ducks/portfolio/candidates.py`
- [x] Export CSV carteira/rebalance — `ducks/portfolio/export_csv.py`
- [x] Persistir preferências no browser (query params) — `ducks/portfolio/persistence.py`
- [x] Suporte completo a BDRs como classe — `DEFAULT_TICKERS_BR_BDRS`
- [x] Threshold de rebalance por desvio % — `rebalance_threshold_pct`
- [x] Moeda-base e conversão cambial (FX) — `shared/utils/fx.py`
- [x] Tickers extras / universo expansível — `parse_extra_tickers`
- [x] Performance e modo rápido de geração — `FETCH_MAX_WORKERS` + `quick_mode`
- [x] Transparência e calibragem do score — `score_breakdown`
- [x] Comparar estratégias lado a lado — `compare_strategies`
- [x] Histórico de runs na sessão — `run_history`
- [x] Persistência robusta de preferências — prefs file + query params
- [x] Onboarding DX (dotenv, README, empty CTAs) — `load_dotenv` em config
- [x] Fatiar UI em módulos (sidebar/results/theme) — `ducks/ui/`
- [x] Data fetcher desacoplado do cache Streamlit — `ducks/market/core.py`
- [x] mypy gradual + teste de integração do pipeline — `mypy.ini` + `test_pipeline_integration`
- [x] Observabilidade de runs / logging estruturado — logging + run_id no pipeline
- [x] Custos de corretagem e IR simplificado (educacional)
- [x] Metas de alocação por classe de ativo — `class_targets`
- [x] Watchlist e alertas técnicos/dividendos — `ducks/portfolio/alerts.py`
- [x] Gráficos de preço no detalhe do ativo
- [x] Explicação de riscos da IA e disclaimer reforçado
- [x] Modo offline e fixtures de mercado — fixtures + core offline
- [x] Docker one-command run — `Dockerfile` + `docker-compose.yml`
- [x] i18n inglês da interface — `ducks/ui/i18n.py`
- [x] Processo jojo-ai (agents.md + system-design + kit + CI)
