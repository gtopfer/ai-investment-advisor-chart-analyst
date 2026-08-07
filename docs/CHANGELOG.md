# Changelog

Todas as mudanças notáveis deste projeto são documentadas aqui. O formato segue livremente o [Keep a Changelog](https://keepachangelog.com/).

Cada entrada deve descrever impacto (o que mudou para usuários/sistema), não detalhe de implementação.

## [Não Lançado]

### Alterado
- **Processo de agentes:** DevKit removido (CLI `./devkit`, pasta `.ai/` de agentes/state, hooks, CI `devkit-review`, guia do usuário DevKit). Projeto passa a usar **jojo-ai** (`agents.md`, `system-design.md`, `CHANGELOG.md` raiz, `kit/`, CI `jojo-review`). Specs de produto migradas para `docs/specs/` e `docs/technical-spec.md`.

### Adicionado
- **SPEC-016…035 (onda completa)**: moeda-base/FX, tickers extras, score transparente + pesos, modo rápido/workers, comparar estratégias, histórico de runs, prefs em arquivo local, dotenv/README/CTAs, UI theme, fetcher core, mypy, logging run_id, custos educacionais, metas por classe, watchlist/alertas, gráficos de preço, riscos IA, offline/fixtures, Docker, i18n PT/EN.
- **SPEC-012**: Exportar carteira alvo e plano de rebalance em CSV (download pós-geração).
- **SPEC-015**: Limiar de rebalance (default 5% do patrimônio alvo); filtra ações com desvio menor.
- **SPEC-014**: Classe **BDRs** com lista padrão B3 (yfinance) e classificação `BDRs`/`BR`.
- **SPEC-013**: Persistência de carteira e preferências no browser (query params); botões salvar/limpar.
- **SPEC-006 [HOTFIX]**: Harness de review estável — `pytest.ini` (pythonpath), lint cobre pacotes do app, testes via `python -m pytest`.
- **SPEC-010**: Aviso na UI quando ativos têm histórico curto demais para indicadores técnicos completos.
- **SPEC-005**: Suporte completo a cripto — lista ampliada, normalização `BTC`→`BTC-USD`, score só técnico (sem penalizar DY=0), preços em USD com aviso de moeda mista.
- **SPEC-001**: Módulo multi-LLM — escolha de provedor Groq ou OpenAI-compatible (Ollama, OpenRouter, etc.), modelo editável na sidebar, chaves via env.
- **SPEC-002**: Layout escuro minimalista — sidebar em seções colapsáveis, empty state guiado, cards de resumo, menos ruído visual.
- **SPEC-003**: Importar carteira atual via CSV/TXT, com modelo baixável e substituição da carteira na sessão.
- **SPEC-004**: Visão **“Como deve ficar”** (atual vs projetado) e botão para aplicar a projeção na carteira da sessão.
- Estrutura inicial do projeto

### Alterado
- **SPEC-007**: Parse de carteira unificado em `portfolio/` (sidebar e import compartilham a mesma lógica).
- **SPEC-008**: Opção **BDRs** removida do multiselect de classes (era opção morta sem candidatos).
- **SPEC-011**: Núcleo de domínio (`classify_ticker`, candidatos, parse) fora de `app.py`; logging no lugar de `print` em erros de ticker.
- Análise de IA desacoplada do SDK Groq via pacote `llm/`.
- Documentação de configuração (`.env.example`, README) para novos provedores e variáveis.

### Removido
- **SPEC-009**: Dependência `plotly` não utilizada (UI segue com `st.bar_chart`).

