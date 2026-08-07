# Especificação de Feature: Layout amigável e minimalista

## 1. Contexto & Valor de Negócio
- **Como um(a)** investidor(a) ou estudante usando o dashboard
- **Eu quero** uma interface limpa, amigável e minimalista (tema escuro)
- **Para que** eu foque nas decisões de carteira e rebalanceamento sem ruído visual, com fluxo fácil de entender

## 2. Requisitos & Restrições

### Requisitos funcionais
1. **Redesign visual minimalista em tema escuro**: hierarquia clara, espaçamento generoso, poucos divisores, paleta sóbria. Não é apenas “dark mode do Streamlit” sem critério — o visual deve parecer intencionalmente limpo.
2. **Preservar 100% das capacidades atuais**: filtros, carteira atual, avançado/IA, gerar carteira, tabela recomendada, gráfico de alocação, plano de rebalanceamento, detalhes técnicos, disclaimer legal. Feature de **UI/UX**, sem mudar regras de score/alocação/dados.
3. **Empty state** na área principal antes de gerar carteira: título curto + 1–2 passos (“ajuste na lateral → Gerar carteira”), sem tela vazia só com disclaimer.
4. **Cards de resumo** após a análise (ex.: quantidade de ativos na carteira alvo, capital/aporte alvo, e se fizer sentido um indicador simples de status da rodada). Métricas derivadas dos dados já existentes — sem novas fontes.
5. **Resultados em seções ordenadas**:
   1. Resumo (métricas)
   2. Carteira recomendada (tabela)
   3. Distribuição de alocação (gráfico)
   4. Plano de rebalanceamento
   5. Detalhes técnicos (recolhido/expander por padrão)
6. **Sidebar em seções colapsáveis**:
   - **Essencial**: classes, universo, estratégia, capital, botão primário de gerar (ou CTA associado)
   - **Carteira atual**: modo + text area de posições
   - **Avançado**: período, IA (e futuros controles multi-LLM da SPEC-001), limites
7. **Copy e decoração sóbrias**: emojis/ícones **mínimos** (quase nenhum); disclaimer pode manter um único aviso visual de atenção se necessário para legibilidade legal, sem poluição.
8. **Status de recomendação legível**: Compra / Aguardar / Venda-Evitar com rótulo textual (cor só como reforço, contraste adequado em fundo escuro).
9. **Disclaimer** permanece visível e inequívoco, com peso visual **secundário** (não compete com a carteira).
10. **Stack**: continuar em **Streamlit** neste MVP (CSS/tema/config + reorganização de componentes em `ui/`). Sem migração de framework.

### Restrições
1. Não alterar pipeline de negócio (`data_fetcher`, `analysis` scores, `allocator`) além do necessário para expor dados já disponíveis à UI.
2. Preferir mudanças em `ui/` (+ tema/CSS Streamlit); `app.py` só orquestra.
3. Coordenação com **SPEC-001** (multi-LLM): o bloco Avançado deve acomodar seletor de provedor/modelo com o mesmo padrão visual quando essa spec for implementada; esta spec não depende da 001 para fechar o layout base.
4. Acessibilidade: contraste legível em tema escuro; não transmitir informação só por cor.

## 3. Expectativas de UI/UX

### Baseline atual
- Título + divider; sidebar densa linear; resultados como subheaders + dataframes; disclaimer em `st.warning` pesado; emojis no título.

### Alvo
| Área | Comportamento |
|------|----------------|
| Header | Compacto: nome do app + subtítulo de uma linha; sem emoji no título (ou no máximo um acento discreto se Streamlit exigir ícone de página) |
| Sidebar | 3 expanders/colapsáveis: Essencial · Carteira atual · Avançado |
| Main (vazio) | Empty state guiado |
| Main (pós-análise) | Métricas → tabela → gráfico → rebalance → expander detalhes |
| Tema | Escuro minimalista (fund, superfícies, texto primário/secundário) |
| Tom | Financeiro limpo; pouco ruído; CTAs claros |

## 4. Checklist Técnico / Notas
- Precisa de mudança no banco de dados: **Não**
- Novos pacotes/dependências: **Não esperado** (Streamlit + CSS custom / `config.toml` se fizer sentido). Architect confirma.
- Regras de segurança/permissão: inalteradas
- Atualizar `.ai/guidelines/design-premises.md` com o padrão visual aprovado (hoje ainda é template genérico)

## 5. Definition of Ready (DoR — Pronto para Começar)
- [x] Problema e resultado desejados claros
- [x] Tema: **escuro minimalista**
- [x] Sidebar: **seções colapsáveis** (Essencial / Carteira / Avançado)
- [x] Escopo MVP: **reorganização + empty state + cards de resumo**
- [x] Emojis: **mínimos / quase nenhum**
- [x] Perguntas em aberto respondidas (2026-07-26)
- [x] Dependências externas: N/A

## 6. Definition of Done (DoD — Pronto/Concluído)
- [x] Todos os requisitos da seção 2 atendidos
- [x] Tema escuro minimalista aplicado de forma coerente (header, sidebar, resultados, disclaimer)
- [x] Empty state visível antes da primeira geração
- [x] Cards de resumo visíveis após análise bem-sucedida
- [x] Sidebar com seções colapsáveis nos três blocos acordados
- [x] Funcionalidades de negócio preservadas; testes existentes passam
- [x] Disclaimer legal presente e legível
- [x] `docs/CHANGELOG.md` atualizado; `design-premises.md` reflete o padrão visual
- [x] Nenhuma regressão conhecida no pipeline de análise

## 7. Critérios de aceitação (rascunho Gherkin)

```gherkin
# language: pt
Funcionalidade: Layout minimalista do dashboard

  Cenário: Estado inicial guiado
    Dado que o usuário abriu o app e ainda não gerou carteira
    Quando a área principal é exibida
    Então deve haver orientação clara de como começar
    E o disclaimer legal permanece acessível

  Cenário: Sidebar organizada
    Dado que o usuário está na tela principal
    Quando ele interage com a sidebar
    Então existem seções distintas para configuração essencial, carteira atual e avançado
    E os controles existentes continuam disponíveis

  Cenário: Resultados após gerar carteira
    Dado que o usuário configurou filtros válidos
    Quando ele gera a carteira recomendada com sucesso
    Então vê um resumo em métricas
    E a carteira recomendada
    E o plano de rebalanceamento (quando aplicável)
    E os detalhes técnicos ficam disponíveis de forma recolhida ou secundária
```

## 8. Decisões de produto fechadas (PM)
| Decisão | Valor |
|---------|--------|
| Tema | Escuro minimalista |
| Sidebar | Colapsável: Essencial / Carteira atual / Avançado |
| Escopo MVP | Reorganização + empty state + cards de resumo |
| Emojis | Mínimos |
| Framework | Streamlit (sem migração) |
| Negócio | Sem mudança de regras de análise/alocação |
