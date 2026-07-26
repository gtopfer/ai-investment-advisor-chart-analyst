# Especificação de Feature: Visão “como deve ficar” (carteira projetada)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário(a) que informou a carteira atual e gerou recomendações
- **Eu quero** ver a carteira **depois** das recomendações e poder **aplicar** essa projeção na carteira da sessão
- **Para que** eu tenha uma visão clara de **“como deve ficar”** e possa simular o estado final (educacional), não só a lista de ordens de compra/venda

## 2. Requisitos & Restrições

### Baseline atual
- **Carteira recomendada**: alocação alvo (`suggested_value` / %).
- **Plano de rebalanceamento**: por ticker, valor atual vs alvo e ação (abrir/comprar mais/reduzir/zerar).
- Falta visão consolidada do **estado final** da carteira e ação para **atualizar** a carteira editável do usuário com esse estado.

### Requisitos funcionais
1. Após análise bem-sucedida, exibir seção **“Como deve ficar”** (carteira projetada).
2. **Tabela comparativa** por ticker com, no mínimo:
   - Ticker  
   - Valor atual (R$)  
   - Valor projetado (R$)  
   - % do total projetado  
   - Variação (R$ e/ou indicação de direção; rótulo textual quando for “Sair”)
3. **Totais** no cabeçalho/resumo da seção: total atual · aporte novo · total projetado (alinhados ao fluxo já calculado: `current_total + capital` ≈ alvo).
4. **Posições a zerar**: permanecem na tabela com valor projetado **0** e indicação clara de **“Sair”** (ou equivalente), para o usuário ver o que deixa a carteira.
5. **Sem carteira atual**: a seção **continua visível**; projeção = carteira recomendada; coluna “atual” em zero/N/A de forma consistente.
6. **Aplicar projeção na carteira atual**:
   - Controle (botão) **“Aplicar na carteira atual”** (copy final na UI pode ser enxuta).
   - Ao acionar: atualiza a carteira da **sessão** (text area / estado usado no próximo “Gerar”) com as posições projetadas de valor **> 0** (modo Valor R$, salvo decisão técnica de formatação).
   - Posições “Sair” **não** entram no texto aplicado (ou entram omitidas — resultado: carteira só com o que permanece).
   - Feedback de sucesso em PT-BR; não grava em disco/banco.
7. **Somente simulação educacional** — não executa ordens em corretora.
8. Coerência com dados já produzidos por alocação + rebalance (`target_values` / `current_values`); evitar números divergentes entre seções na mesma rodada.
9. Encaixe na hierarquia de resultados (SPEC-002): após plano de rebalanceamento ou imediatamente associado a ele.

### Restrições
1. Não alterar fórmulas de score/alocação além do necessário para montar a visão projetada.
2. Sem API de corretora; sem persistência entre sessões de navegador.
3. Aplicar na carteira é **opt-in** (botão); não sobrescrever a carteira do usuário automaticamente ao gerar resultados.

## 3. Expectativas de UI/UX
| Elemento | Comportamento |
|----------|----------------|
| Título da seção | “Como deve ficar” (ou “Carteira projetada”) |
| Resumo | Métricas: atual / aporte / projetado |
| Tabela | Atual vs projetado + % + variação; linha “Sair” quando projetado = 0 e havia posição |
| CTA | Botão secundário: aplicar projeção na carteira da sessão |
| Tom | Alinhado ao minimalismo (SPEC-002); poucos emojis |

## 4. Checklist Técnico / Notas
- Banco: **Não**
- Dependências novas: **Não esperado**
- Função pura sugerida: `build_projected_portfolio(current_values, target_assets) -> rows` (testável)
- UI: `display_projected_portfolio(...)` em `ui/`; handler de “aplicar” atualiza session state da text area
- Coordenação SPEC-003: após aplicar, o texto fica no mesmo formato importável/editável

## 5. Definition of Ready (DoR — Pronto para Começar)
- [x] Problema e valor claros
- [x] Escopo: **visualização + aplicar na carteira**
- [x] Tabela: **Atual vs Projetado + %**
- [x] Zerar: **mostrar com projetado 0 / “Sair”**
- [x] Sem carteira atual: **projeção = recomendada, seção visível**
- [x] Aplicar é opt-in (botão), não automático
- [x] Perguntas respondidas (2026-07-26)

## 6. Definition of Done (DoD — Pronto/Concluído)
- [x] Seção “Como deve ficar” após gerar carteira, com tabela e totais coerentes
- [x] Linhas de saída (“Sair”) visíveis quando aplicável
- [x] Sem carteira atual: projeção ainda exibida a partir da recomendada
- [x] Botão aplica projeção (valor > 0) na carteira da sessão e usuário pode re-gerar
- [x] Testes da montagem projetada + comportamento de aplicar (onde testável)
- [x] `docs/CHANGELOG.md` (+ README se necessário)
- [x] Sem regressão em carteira recomendada / rebalanceamento

## 7. Critérios de aceitação (rascunho Gherkin)

```gherkin
# language: pt
Funcionalidade: Carteira projetada ("como deve ficar")

  Cenário: Ver comparativo após gerar com carteira atual
    Dado que o usuário informou posições atuais e um aporte
    Quando ele gera a carteira recomendada com sucesso
    Então vê a seção "Como deve ficar"
    E cada ticker relevante mostra valor atual, valor projetado e percentual projetado

  Cenário: Posição a zerar aparece como Sair
    Dado que um ticker da carteira atual não entra no alvo (ou alvo zero)
    Quando a projeção é exibida
    Então esse ticker aparece com valor projetado zero e indicação de saída

  Cenário: Sem carteira atual ainda há projeção
    Dado que o usuário não informou posições atuais
    Quando a carteira recomendada é gerada
    Então a seção "Como deve ficar" reflete a carteira alvo recomendada

  Cenário: Aplicar projeção atualiza a carteira da sessão
    Dado que a projeção foi exibida com posições de valor positivo
    Quando o usuário aciona "Aplicar na carteira atual"
    Então a carteira editável da sessão passa a refletir essas posições
    E posições apenas de saída não permanecem como posição ativa
```

## 8. Decisões de produto fechadas (PM)
| Decisão | Valor |
|---------|--------|
| Escopo | Visualizar projeção **+** aplicar na carteira (opt-in) |
| Tabela | Atual vs Projetado + % (+ variação / “Sair”) |
| Zerar | Mostrar com projetado 0 e rótulo “Sair” |
| Sem carteira atual | Projeção = recomendada; seção visível |
| Aplicar automático | **Não** — só via botão |
| Corretora | Fora de escopo (simulação educacional) |
