# AGENTS.MD

Régua universal + Especificação do Projeto.  
**Processo:** [jojo-ai](https://github.com/gtopfer/jojo-ai) · versão 1.4

---

## 🎯 Como Usar (humano)

1. Preencha **Seção 1** (projeto + **Features**)
2. Preencha **`system-design.md`** (arquitetura / design system)
3. Diga à IA: **"siga agents.md"**
4. A IA lê as Features abaixo, mapeia e começa o loop (com seu OK no chat)

**Onde escrever a NOVA FEATURE:**  
→ **Seção 1 → `### Features`** (lista com `- [ ]` / `- [x]`)

Não precisa criar arquivo em outro lugar para “pedir” a feature. A IA mapeia dali.

---

## 📋 SEÇÃO 1: PROJETO

### Projeto: AI Investment Advisor & Chart Analyst

**Stack:**

- Frontend / App: Streamlit (Python 3.11+)
- Backend: N/A (pipeline no mesmo processo Streamlit)
- Database: Nenhuma (stateless; cache TTL + session state)
- Dados: yfinance (Yahoo Finance)
- IA: Groq / OpenAI-compatible via pacote `llm/`
- Testes / Lint: pytest + ruff
- CI/CD: GitHub Actions (`jojo-review.yml` + suite Python)

**Contexto:**
Dashboard educacional de análise de investimentos: indicadores técnicos (RSI, MACD, EMAs, Bollinger), dividendos, interpretação por IA, scoring e alocação de carteira com plano de rebalanceamento. Mercados BR (ações/FIIs/BDRs), US (ações/ETFs) e cripto.

**Usuários:**
Investidores em aprendizado e uso pessoal/demo — não é recomendação profissional de investimento.

**Guardrails Obrigatórios:**

- Ducks Pattern: código de feature em `ducks/<domínio>/` com API pública em `__init__.py` — ver `system-design.md` §2
- Shared só para config/models/utils (`shared/`)
- Sem lógica de negócio em `ducks/ui/`; sem yfinance/LLM direto na UI
- `shared/models` sem dependências de ducks
- Chaves de API e senhas só via env (nunca hardcoded / query params)
- Disclaimer educacional sempre visível; sem tom de “dica de compra”
- TDD para feature nova ou regressão relevante

**Convenções:**

- Naming: snake_case (Python); um duck por domínio
- Code style: ruff (lint + format)
- Testes em `tests/`; fixtures de mercado em `tests/fixtures/`
- Histórico de specs: `docs/specs/`; detalhe técnico: `docs/technical-spec.md`
- Processo de agentes: **jojo-ai** — humano edita só `agents.md` + `system-design.md` + `CHANGELOG.md`

---

### Features

> **VOCÊ ESCREVE A FEATURE AQUI.**  
> A IA usa esta lista como backlog: pega o **primeiro** `- [ ]`, mapeia, pede OK e entra no ciclo (spec → UX → arch → TDD → código).

**Como escrever (um item por feature):**

```markdown
- [ ] Título curto — o que o usuário ganha (1 linha). Detalhe opcional: quem usa, regra importante, fora de escopo.
- [x] Feature já entregue (a IA marca [x] quando done)
```

#### Pendente (próximo trabalho)

<!-- Adicione `- [ ] …` aqui. Sem itens abertos, a IA pergunta o que fazer. -->

#### Entregue (auditado 2026-08-07 — código + testes OK)

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

---

## 📋 SEÇÃO 2: REGRAS DE AGENTES (Não Altere)

### Princípio de UX

```
Humano escreve features → agents.md Seção 1 · ### Features
Humano escreve design   → system-design.md
Agentes leem, mapeiam, pedem OK, executam, marcam [x]
```

- **Fonte da verdade do backlog = `### Features` neste arquivo.**  
- Nunca peça ao humano outro arquivo só para “cadastrar” feature.  
- Agente **pode** gerar artefatos internos (ex.: rascunho em `docs/specs/…`) — o humano **não** é obrigado a abrir isso.

### Bootstrap (agentes / CI)

```bash
cd kit && npm run sync
```

### 8 Fases

```
draft → spec_approved → ux_approved → tech_approved → test_red → code_review → tested → done
```

### 6 Agentes

| Fase | Agente | Runbook |
| --- | --- | --- |
| draft | Product Manager | `kit/docs/agents/product-manager.agent.md` |
| spec_approved | UX Designer | `kit/docs/agents/ux-designer.agent.md` |
| ux_approved | Architect | `kit/docs/agents/architect.agent.md` |
| tech_approved | QA | `kit/docs/agents/qa.agent.md` |
| test_red | Developer | `kit/docs/agents/developer.agent.md` |
| code_review | QA | `kit/docs/agents/qa.agent.md` |
| tested | Product Manager | `kit/docs/agents/product-manager.agent.md` |
| (sempre) | Squad Lead | `kit/docs/agents/squad-lead.agent.md` |

### Skills

Catálogo: `kit/generated/skills-registry.json`  
`tdd` · `code-review` · `ui-ux` · `ducks-pattern` · `autonomous-loop` · `microcopy`

### 5 Princípios

1. Simplicidade  
2. Sem laziness (causa raiz)  
3. Impacto mínimo  
4. Reversibilidade  
5. Verificação (testes verdes)

---

## 🔄 FLUXO (Para Agentes)

```
1. Lê agents.md SEÇÃO 1 (projeto)
2. Lê ### Features  ← backlog humano
3. Lê system-design.md
4. Pega o PRIMEIRO item - [ ] (não feito)
5. Apresenta resumo + plano no chat → AGUARDA OK do humano
6. Executa 8 fases (PM → … → done)
7. Marca - [x] na ### Features e registra em CHANGELOG.md
```

### Checklist

- [ ] Leu **### Features** em agents.md  
- [ ] Leu system-design.md  
- [ ] Feature nova = primeiro `- [ ]`  
- [ ] OK humano no chat antes de codar  
- [ ] Ao terminar: `- [x]` em Features + CHANGELOG  

---

## 📌 Resposta em uma linha

**Nova feature → Seção 1 → `### Features` → item `- [ ] ...`**

**Versão:** 1.4 | Backlog humano = `### Features`  
**Última auditoria Features:** 2026-08-07 (Ducks Pattern entregue; suite pytest verde)
