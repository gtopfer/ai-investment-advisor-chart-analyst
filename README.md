# AI Investment Advisor & Chart Analyst 📈🤖

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B)](https://streamlit.io/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-lightgrey.svg)](LICENSE)

Dashboard de análise de investimentos que combina **análise técnica** (RSI, MACD, EMAs, Bandas de Bollinger), **análise fundamentalista de dividendos** e **interpretação por IA generativa** (Groq Cloud / Llama 3.3) para sugerir alocação de portfólio e plano de rebalanceamento, com base na estratégia e no capital informados pelo usuário.

> ⚠️ **Disclaimer**: ferramenta de finalidade estritamente **educacional**. Nada aqui constitui recomendação de compra ou venda de ativos. Rentabilidade passada não garante resultados futuros. Consulte um profissional certificado antes de investir.

---

## Sumário

- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#️-arquitetura)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#️-uso)
- [Guia da Interface](#-guia-da-interface)
- [Testes e Lint](#-testes-e-lint)
- [Limitações Conhecidas](#-limitações-conhecidas)
- [Contribuindo](#-contribuindo)
- [Licença](#licença)

---

## 🚀 Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| **Análise Técnica Automatizada** | RSI, MACD, tendência de EMAs (20/50/200), Bandas de Bollinger, volatilidade anualizada e níveis de suporte/resistência, via `pandas-ta` |
| **Interpretação por IA Generativa** | Provedor configurável (Groq ou OpenAI-compatible) interpreta indicadores e devolve tendência, confiança e resumo em PT-BR — limite de chamadas por sessão e senha opcional |
| **Análise de Dividendos** | Dividend Yield normalizado, score 0–1, consistência histórica de pagamento e flag de volatilidade |
| **Alocação de Portfólio** | Scoring ponderado por estratégia (Growth / Dividendos / Equilíbrio) e distribuição proporcional de capital entre os ativos elegíveis |
| **Plano de Rebalanceamento** | Compara a carteira atual informada com a carteira alvo sugerida e gera as ações necessárias (comprar/reduzir/zerar) |
| **Como deve ficar** | Visão projetada da carteira (atual vs alvo) com opção de aplicar a projeção na carteira da sessão |
| **Importar carteira** | Upload CSV/TXT + modelo baixável para preencher a carteira atual |
| **UI minimalista** | Tema escuro, sidebar colapsável, empty state e cards de resumo |
| **Coleta Paralela** | Preços, fundamentos e histórico de dividendos buscados em paralelo (`ThreadPoolExecutor`) com cache de 15 min e retry automático |

Cobertura de mercado: ações e FIIs brasileiros (B3), ações e ETFs americanos, e **criptoativos** (via yfinance: `BTC-USD` ou atalho `BTC`, lista padrão ampliada, score técnico sem penalidade de dividendos).

---

## 🛠️ Arquitetura

Pipeline de dados em camadas funcionais — sem persistência, sem framework backend separado:

```text
ai-investment-advisor-chart-analyst/
├── app.py                      # Orquestrador: entrypoint Streamlit, monta o pipeline
├── config/
│   └── config.py               # Configuração global, tickers padrão, pesos de estratégia
├── data_fetcher/
│   └── market_data.py          # Coleta via yfinance (cache 15min + retry)
├── analysis/
│   ├── technical_analysis.py   # Indicadores técnicos (pandas-ta)
│   ├── dividend_analysis.py    # Análise de proventos
│   └── ai_chart_engine.py      # Orquestra prompt/parse e delega ao provedor LLM
├── llm/
│   └── ...                     # Adapters Groq e OpenAI-compatible + registry
├── portfolio/
│   └── import_portfolio.py     # Import CSV/TXT da carteira atual
├── allocator/
│   └── portfolio_allocator.py  # Scoring, alocação, rebalance e projeção
├── models/
│   └── schemas.py              # Dataclasses de contrato entre camadas
└── ui/
    └── layout.py               # Tema escuro, sidebar e resultados
```

Documentação técnica completa (diagramas, contratos de interface, decisões arquiteturais e riscos mapeados) em [`docs/technical-spec.md`](docs/technical-spec.md). Arquitetura e design system em [`system-design.md`](system-design.md). Processo de agentes **jojo-ai v1.4**: edite Features em [`agents.md`](agents.md) e diga *siga agents.md* — ver também [`docs/README.md`](docs/README.md).

---

## 💻 Requisitos

- Linux, macOS ou Windows
- Python 3.11+
- Chave de API de LLM opcional (Groq e/ou endpoint OpenAI-compatible) — Groq grátis em [console.groq.com](https://console.groq.com/keys)

---

## 📦 Instalação

```bash
git clone https://github.com/gtopfer/ai-investment-advisor-chart-analyst.git
cd ai-investment-advisor-chart-analyst
```

**Criar e ativar ambiente virtual:**

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

**Instalar dependências:**

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração

Copie o template de variáveis de ambiente e preencha o que precisar:

```bash
cp .env.example .env
```

| Variável | Obrigatória | Descrição |
|---|---|---|
| `GROQ_API_KEY` | Não | Habilita o provedor Groq |
| `GROQ_MODEL` | Não | Modelo Groq (padrão: `llama-3.3-70b-versatile`) |
| `OPENAI_API_KEY` | Não | Chave para endpoint OpenAI-compatible (pode ficar vazia em Ollama local) |
| `OPENAI_BASE_URL` | Não | Base URL OpenAI-compatible (ex.: `http://localhost:11434/v1`) |
| `OPENAI_MODEL` | Não | Modelo default do provedor OpenAI-compatible |
| `LLM_PROVIDER` | Não | Preferência: `groq` ou `openai_compatible` quando ambos existem |
| `AI_ACCESS_PASSWORD` | Não | Se definida, exige senha na sidebar antes de liberar chamadas à IA |
| `MAX_AI_CALLS_PER_SESSION` | Não | Limite de chamadas à IA por sessão (padrão: `15`) |

`streamlit run` não carrega `.env` automaticamente — exporte as variáveis no shell antes de rodar, ou use uma ferramenta como `python-dotenv`/`direnv` se preferir carregamento automático.

```bash
# Linux/macOS
export GROQ_API_KEY="sua_chave_aqui"

# Windows (PowerShell)
$env:GROQ_API_KEY="sua_chave_aqui"
```

---

## ▶️ Uso

Com o ambiente virtual ativado e as dependências instaladas:

```bash
streamlit run app.py
```

O navegador abre automaticamente em `http://localhost:8501`.

---

## 📖 Guia da Interface

1. **Sidebar — Essencial**
   - Classes (Ações, FIIs, ETFs, BDRs, Cripto), universo, estratégia, aporte e **moeda-base** (BRL/USD)

2. **Sidebar — Carteira**
   - Posições, import CSV/TXT, **tickers extras**, **watchlist**

3. **Sidebar — Avançado**
   - Período, limiar de rebalance, modo rápido, comparar estratégias, IA, pesos do score, metas por classe

4. **Preferências**
   - Salvar/limpar em arquivo local + URL (sem senhas/API keys)

5. **Gerar carteira**
   - Métricas → carteira (CSV) → rebalance (CSV + custo est.) → projeção → comparação → alertas → detalhes (breakdown, gráfico) → histórico de runs

---

## 🧪 Testes e Lint

```bash
pip install -r requirements-dev.txt
pytest -q
ruff check .
```

---

## ⚠️ Limitações Conhecidas

- `yfinance` é uma biblioteca não-oficial (depende de scraping do Yahoo Finance) — sujeita a instabilidade e mudanças sem aviso. Mitigado com cache de 15 min e retry automático
- Sem autenticação real de usuário — a `AI_ACCESS_PASSWORD` é apenas uma barreira simples para limitar uso indevido de quota
- Indicadores técnicos exigem ao menos 50 candles de histórico; ativos com histórico curto retornam valores neutros silenciosamente
- Sem persistência — nada é salvo entre sessões

Detalhamento completo de riscos e mitigações em [`docs/technical-spec.md`](docs/technical-spec.md#8-riscos-e-mitigações).

---

## 🤝 Contribuindo

Projeto modular — pontos de extensão comuns:

- Novos indicadores técnicos → `analysis/technical_analysis.py`
- Ajustes no prompt/parsing da IA → `analysis/ai_chart_engine.py`
- Novas fontes de dados de mercado → `data_fetcher/`
- Novos tickers padrão ou pesos de estratégia → `config/config.py`

Antes de abrir um PR, rode `pytest -q` e `ruff check .` localmente.

---

## Licença

Licenciado sob a [GNU General Public License v3.0](LICENSE).

**Desenvolvido por [GTopfer](https://github.com/gtopfer), com AI.**
