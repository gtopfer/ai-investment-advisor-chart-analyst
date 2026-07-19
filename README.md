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
| **Interpretação por IA Generativa** | Groq Cloud (Llama 3.3 70B) lê os indicadores técnicos e devolve tendência, confiança e resumo em PT-BR — com limite de chamadas por sessão e senha de acesso opcional |
| **Análise de Dividendos** | Dividend Yield normalizado, score 0–1, consistência histórica de pagamento e flag de volatilidade |
| **Alocação de Portfólio** | Scoring ponderado por estratégia (Growth / Dividendos / Equilíbrio) e distribuição proporcional de capital entre os ativos elegíveis |
| **Plano de Rebalanceamento** | Compara a carteira atual informada com a carteira alvo sugerida e gera as ações necessárias (comprar/reduzir/zerar) |
| **Coleta Paralela** | Preços, fundamentos e histórico de dividendos buscados em paralelo (`ThreadPoolExecutor`) com cache de 15 min e retry automático |

Cobertura de mercado: ações e FIIs brasileiros (B3), ações e ETFs americanos, e criptoativos (via yfinance).

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
│   └── ai_chart_engine.py      # Integração com Groq API
├── allocator/
│   └── portfolio_allocator.py  # Scoring, alocação de capital e rebalanceamento
├── models/
│   └── schemas.py              # Dataclasses de contrato entre camadas
└── ui/
    └── layout.py               # Componentes visuais do Streamlit
```

Documentação técnica completa (diagramas, contratos de interface, decisões arquiteturais e riscos mapeados) em [`.ai/technical-spec.md`](.ai/technical-spec.md). O projeto segue um fluxo de desenvolvimento orientado a especificação — ver [`docs/README.md`](docs/README.md).

---

## 💻 Requisitos

- Linux, macOS ou Windows
- Python 3.11+
- Chave de API Groq (opcional, só para as funcionalidades de IA) — grátis em [console.groq.com](https://console.groq.com/keys)

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
| `GROQ_API_KEY` | Não | Habilita a análise de IA. Sem ela, o app funciona normalmente, mas a coluna "Motivo" fica sem os insights gerados por IA |
| `AI_ACCESS_PASSWORD` | Não | Se definida, exige senha na sidebar antes de liberar chamadas à IA |
| `MAX_AI_CALLS_PER_SESSION` | Não | Limite de chamadas à Groq por sessão (padrão: `15`) — protege sua quota/custo |

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

1. **Sidebar — Filtros**
   - **Classes de Ativos**: Ações, FIIs, ETFs, Cripto
   - **Universo**: Nacional (B3), Internacional (US) ou Ambos
   - **Estratégia**: *Growth* (peso técnico 0.8), *Dividendos* (peso dividendo 0.7) ou *Equilíbrio* (50/50)
   - **Capital**: novo aporte a simular (R$)

2. **Sidebar — Carteira Atual**
   - Informe as posições atuais (uma por linha, `TICKER, VALOR` ou `TICKER, QUANTIDADE`) para gerar o plano de rebalanceamento comparando com a carteira alvo

3. **Sidebar — Avançado**
   - Período de análise, ativação da IA (com senha, se configurada), limite de ativos analisados por IA, e máximo de ativos na carteira final

4. **Gerar Carteira Recomendada**
   - Clique no botão da sidebar e aguarde o processamento (a coleta é paralela, mas chamadas de IA são sequenciais)
   - A tabela final mostra recomendação (Compra / Aguardar / Venda-Evitar), score, alocação % e valor sugerido, seguida do plano de rebalanceamento e do detalhe técnico de cada ativo

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

Detalhamento completo de riscos e mitigações em [`.ai/technical-spec.md`](.ai/technical-spec.md#8-riscos-e-mitigações).

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
