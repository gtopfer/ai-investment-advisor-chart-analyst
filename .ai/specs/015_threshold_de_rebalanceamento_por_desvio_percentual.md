# Especificação de Feature: Threshold de rebalanceamento por desvio percentual

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário que rebalanceia com disciplina
- **Eu quero** só ver ações de comprar/vender quando o desvio em relação ao alvo superar um limiar %
- **Para que** eu ignore ruído de rebalance de poucos reais/percentuais

## 2. Requisitos & Restrições
- **R1**: Controle na UI (sidebar ou bloco de rebalance) para limiar de desvio **0–20%**, passo razoável (ex. 0,5 ou 1).
- **R2**: **Default = 5%** (decisão 2026-08-01).
- **R3**: O plano de rebalance **filtra** (não apenas marca) ações cujo desvio relativo ao alvo fica **abaixo** do limiar. Definição observável do desvio: percentual do valor alvo da posição (ou do patrimônio total — **fixixar no Architect**; default de negócio: `|delta| / max(valor_alvo, epsilon)` ou `|peso_atual − peso_alvo|` — preferir **desvio de peso no total da carteira alvo** se já existir no modelo; senão documentar fórmula única na tech-spec).
- **R4**: Se **todas** as ações forem filtradas: mensagem empty clara (ex. “Nenhuma ação acima do limiar de X%”).
- **R5**: Limiar 0% reproduz o comportamento atual (todas as ações relevantes do motor).
- **R6**: Export (SPEC-012), se existir, exporta o plano **já filtrado** como exibido.
- **Restrição**: Não altera scoring/alocação alvo — só a **apresentação/filtro** do plano de ações (ou o builder do plano com parâmetro threshold).
- **Fora de escopo**: rebalance tax-aware, lotes mínimos de corretora.

## 3. Expectativas de UI/UX
- **Há interface de usuário?** Sim
- Controle de limiar + tabela filtrada + empty state
- Microcopy: “Ignorar desvios menores que X%”

### Definition of Done — UX
- [ ] Controle e empty definidos
- [ ] Microcopy
- [ ] design-premises
- [ ] Aceite UX

## 4. Checklist Técnico / Notas
- Banco: Não
- Pacotes: Não
- Ponto: `build_rebalance_actions` ou filtro pós-build + param na UI

## 5. Definition of Ready (DoR)
- [x] Claro
- [x] Default 5%, filtra, 0–20%
- [x] Fórmula exata do % a fechar no Architect com base no modelo atual

## 6. Definition of Done (DoD)
- [ ] R1–R6 atendidos
- [ ] Testes unitários do filtro (0%, 5%, tudo filtrado)
- [ ] CHANGELOG; review APROVADO
