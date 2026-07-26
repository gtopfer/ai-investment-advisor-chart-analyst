# Premissas de Design & Produto

Este arquivo contém as diretrizes permanentes de UI/UX, regras de design system e premissas gerais do produto.

> **Atenção IA**: Toda decisão de design de interface, fluxo de usuário, escolhas de bibliotecas visuais ou arquitetura técnica deve obrigatoriamente respeitar as premissas descritas neste documento.

---

## 1. Premissas de UI (Interface do Usuário) & Design System

- **Biblioteca de UI/UX**: Streamlit nativo + CSS custom (tema escuro minimalista)
- **Temas**: Dark mode padrão (fundo `#0f1419`, superfícies `#151b23`, bordas `#243041`, texto `#e7ecf1`)
- **Tipografia**: Hierarquia Streamlit; títulos sem emoji decorativo; subtítulo discreto
- **Cores**:
  - Fundo: `#0f1419`
  - Superfície/sidebar: `#151b23`
  - Texto primário: `#e7ecf1`
  - Texto secundário: `#8b9bb0`
- **Emojis/ícones**: mínimos; preferir copy sóbria

---

## 2. Premissas de UX (Experiência do Usuário)

- **Navegação**: Sidebar em seções colapsáveis — Essencial · Carteira atual · Avançado
- **Empty state**: orientação em 3 passos antes da primeira análise
- **Resultados**: métricas de resumo → carteira → alocação → rebalanceamento → “Como deve ficar” → detalhes técnicos (expander)
- **Estados de interação**:
  - Spinner + progress bar durante análise
  - Import de carteira com feedback de N importadas / M ignoradas
  - Fallback de IA com mensagem em PT-BR sem quebrar o fluxo

---

## 3. Premissas Técnicas Globais & de Engenharia

- **Stack UI**: Streamlit single-page; sem SPA separado no MVP
- **Persistência**: nenhuma entre sessões (session state apenas)
- **LLM**: módulo `llm/` pluggável (Groq + OpenAI-compatible); chaves só via env
- **Acessibilidade**: contraste legível no tema escuro; status de recomendação sempre com rótulo textual
