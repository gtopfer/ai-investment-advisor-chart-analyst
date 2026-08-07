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

- Pipeline em camadas funcionais (`config → data_fetcher → analysis → allocator → models → ui`, orquestrado por `app.py`)
- Sem lógica de negócio em `ui/`; sem yfinance/LLM direto na UI
- `models/schemas.py` sem dependências internas do projeto
- Chaves de API e senhas só via env (nunca hardcoded / query params)
- Disclaimer educacional sempre visível; sem tom de “dica de compra”
- TDD para feature nova ou regressão relevante

**Convenções:**

- Naming: snake_case (Python); pacotes por camada funcional
- Code style: ruff (lint + format)
- Testes em `tests/`; fixtures de mercado em `tests/fixtures/`
- Histórico de specs: `docs/specs/`; detalhe técnico: `docs/technical-spec.md`
- Processo de agentes: **jojo-ai** — humano edita só `agents.md` + `system-design.md` + `CHANGELOG.md`

---

### Features

> **VOCÊ ESCREVE A FEATURE AQUI.**  
> A IA usa esta lista como backlog: pega o primeiro `- [ ]`, mapeia, pede OK e entra no ciclo (spec → UX → arch → TDD → código).

**Como escrever (um item por feature):**

```markdown
- [ ] Título curto — o que o usuário ganha (1 linha). Detalhe opcional: quem usa, regra importante, fora de escopo.
- [x] Feature já entregue (a IA marca [x] quando done)
```

**Backlog / histórico (edite isto):**

#### Entregue (base + higiene + onda 012–035)

- [x] Multi-LLM (Groq + OpenAI-compatible) — escolher provedor/modelo na sidebar
- [x] Layout minimalista escuro — sidebar colapsável, empty state, cards
- [x] Importar carteira atual via CSV/TXT + modelo baixável
- [x] Visão “Como deve ficar” (projetada) e aplicar na sessão
- [x] Suporte a cripto (normalização -USD, score só técnico)
- [x] Harness de testes/lint estável (pytest path + ruff)
- [x] Parse de carteira unificado em `portfolio/`
- [x] Remover BDRs mortos do multiselect (depois: BDRs reais)
- [x] Remover dependência plotly não usada
- [x] Avisos de qualidade de dados (histórico curto)
- [x] Extrair núcleo de domínio de `app.py` + logging
- [x] Export CSV carteira/rebalance
- [x] Persistir preferências no browser (query params)
- [x] Suporte completo a BDRs como classe
- [x] Threshold de rebalance por desvio %
- [x] Moeda-base e conversão cambial (FX)
- [x] Tickers extras / universo expansível
- [x] Performance e modo rápido de geração
- [x] Transparência e calibragem do score
- [x] Comparar estratégias lado a lado
- [x] Histórico de runs na sessão
- [x] Persistência robusta de preferências
- [x] Onboarding DX (dotenv, README, empty CTAs)
- [x] Fatiar UI em módulos (sidebar/results/theme)
- [x] Data fetcher desacoplado do cache Streamlit
- [x] mypy gradual + teste de integração do pipeline
- [x] Observabilidade de runs / logging estruturado
- [x] Custos de corretagem e IR simplificado (educacional)
- [x] Metas de alocação por classe de ativo
- [x] Watchlist e alertas técnicos/dividendos
- [x] Gráficos de preço no detalhe do ativo
- [x] Explicação de riscos da IA e disclaimer reforçado
- [x] Modo offline e fixtures de mercado
- [x] Docker one-command run
- [x] i18n inglês da interface
- [x] Processo jojo-ai (agents.md + system-design + kit + CI)

#### Pendente (próximo trabalho)

<!-- Adicione itens com "- [ ] …". Se não houver nenhum - [ ], a IA pergunta o que fazer em vez de inventar feature. -->

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
