# AI Investment Advisor & Chart Analyst 📈🤖

Bem-vindo ao **AI Investment Advisor**, um sistema inteligente de análise de investimentos projetado para fins educacionais. Este projeto utiliza Python, Streamlit e Inteligência Artificial (Groq Cloud com Llama 3) para analisar ativos financeiros, interpretar gráficos técnicos e sugerir alocações de portfólio baseadas em estratégias personalizadas.

> ⚠️ **DISCLAIMER**: Esta ferramenta tem finalidade estritamente **EDUCACIONAL**. Os dados apresentados não constituem recomendação de compra ou venda de ativos. Rentabilidade passada não é garantia de resultados futuros. Consulte um profissional certificado antes de investir.

---

## 🚀 Funcionalidades

1. **Análise Técnica Automatizada**: Cálculo de indicadores como RSI, MACD, Bandas de Bollinger e EMAs usando `pandas-ta`.
2. **Inteligência Artificial Generativa**: Integração com a Groq Cloud (Llama 3) para interpretar padrões gráficos e fornecer resumos em linguagem natural (PT-BR).
3. **Análise Fundamentalista (Dividendos)**: Avaliação de Dividend Yield e consistência de pagamentos.
4. **Alocação de Portfólio Inteligente**: Algoritmo de scoring que pondera fatores técnicos e fundamentalistas conforme o perfil do usuário (Growth, Dividendos ou Equilíbrio).
5. **Interface Interativa**: Dashboard moderno construído com Streamlit.

---

## 🛠️ Arquitetura do Sistema

O projeto é modular e organizado da seguinte forma:

```text
/AI-Investment-Advisor-Chart-Analyst
├── app.py                      # Ponto de entrada da aplicação Streamlit
├── requirements.txt            # Dependências do projeto
├── config/
│   └── config.py               # Configurações globais, tickers padrão e pesos
├── data_fetcher/
│   └── market_data.py          # Coleta de dados via yfinance
├── analysis/
│   ├── technical_analysis.py   # Cálculos técnicos (pandas-ta)
│   ├── dividend_analysis.py    # Análise de proventos
│   └── ai_chart_engine.py      # Integração com Groq API
├── allocator/
│   └── portfolio_allocator.py  # Lógica de scoring e alocação de capital
├── models/
│   └── schemas.py              # Definição de classes de dados (Data Classes)
└── ui/
    └── layout.py               # Componentes visuais do Streamlit
```

---

## 💻 Requisitos de Sistema

- **Sistema Operacional**: Linux, macOS ou Windows.
- **Python**: Versão 3.11 ou superior.
- **Chave de API Groq**: Necessária para as funcionalidades de IA (gratuita em [console.groq.com](https://console.groq.com)).

---

## 📦 Instalação Passo a Passo

Siga os passos abaixo para rodar o projeto localmente.

### 1. Clonar o Repositório

Se você tiver o git instalado:

```bash
git clone https://github.com/seu-usuario/AI-Investment-Advisor-Chart-Analyst.git
cd AI-Investment-Advisor-Chart-Analyst
```

Ou simplesmente baixe e extraia os arquivos na pasta desejada.

### 2. Criar Ambiente Virtual (Recomendado)

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Opcional (para facilitar localmente): copie o exemplo e edite:

```bash
cp .env.example .env
```

Para usar a IA da Groq (Llama 3), você precisa de uma API Key. Obtenha uma gratuitamente em [Groq Console](https://console.groq.com/keys).

**Linux/macOS:**

```bash
export GROQ_API_KEY="sua_chave_aqui"
```

**Windows (PowerShell):**

```powershell
$env:GROQ_API_KEY="sua_chave_aqui"
```

> **Nota**: Se não configurar a chave, o sistema funcionará, mas a coluna "Motivo" não terá os insights gerados pela IA.

---

## ▶️ Como Rodar

Com o ambiente virtual ativado e as dependências instaladas, execute:

```bash
streamlit run app.py
```

O navegador abrirá automaticamente no endereço `http://localhost:8501`.

---

## 🧪 Testes rápidos e lint

Instale as dependências de desenvolvimento e rode os testes unitários básicos:

```bash
pip install -r requirements-dev.txt
pytest -q
```

Use `ruff check .` para um lint rápido.

---

## 📖 Guia de Uso

1. **Barra Lateral (Sidebar)**:
    - **Classes de Ativos**: Selecione o que deseja analisar (Ações, FIIs, Cripto, etc.).
    - **Universo**: Escolha entre ativos Nacionais (B3), Internacionais (US) ou Ambos.
    - **Estratégia**:
        - *Growth*: Foca em tendências de alta e indicadores técnicos fortes.
        - *Dividendos*: Prioriza DY e estabilidade.
        - *Equilíbrio*: Meio termo.
    - **Capital**: Insira o valor que deseja simular (ex: R$ 10.000).

2. **Gerar Carteira**:
    - Clique no botão **"Gerar Carteira Recomendada"**.
    - Aguarde o processamento (pode levar alguns segundos devido às chamadas de API).

3. **Interpretar Resultados**:
    - Uma tabela será exibida com os ativos recomendados, ação sugerida (Compra/Aguardar), alocação ideal e motivos.
    - Gráficos de distribuição mostrarão como dividir o capital.

---

## ⚙️ Configuração Avançada

Você pode personalizar o comportamento do sistema editando o arquivo `config/config.py`:

- **Adicionar novos ativos**: Edite as listas `DEFAULT_TICKERS_...`.
- **Ajustar pesos**: Altere o dicionário `STRATEGY_WEIGHTS` para mudar a importância da análise técnica vs. dividendos.
- **Limiares**: Modifique `MIN_DY_THRESHOLD` ou `RSI_OVERBOUGHT` conforme sua preferência.
- **Modelo de IA**: Altere `GROQ_MODEL_NAME` para testar outros modelos (ex: `llama3-8b-8192`).

---

## 🤝 Contribuições

Este projeto foi construído com modularidade em mente. Sinta-se à vontade para:

- Adicionar novos indicadores em `analysis/technical_analysis.py`.
- Melhorar o prompt da IA em `analysis/ai_chart_engine.py`.
- Implementar conectores para outras fontes de dados em `data_fetcher/`.

---

**Desenvolvido por GTopfer, com AI**
