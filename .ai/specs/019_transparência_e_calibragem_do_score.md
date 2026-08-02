# Especificação de Feature: Transparência e calibragem do score

> **Prioridade:** P0 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário que questiona caixa-preta de recomendação
- **Eu quero** ver breakdown do score e opcionalmente ajustar pesos
- **Para que** eu confie ou personalize a lógica de ranking

## 2. Requisitos & Restrições
- **R1**: Cada ativo pontuado expõe componentes (ex. RSI, MACD, EMA, IA, dividendos) com contribuições numéricas.
- **R2**: UI: no expander de detalhes, tabela/lista do breakdown.
- **R3**: Avançado: editar pesos technical/dividend da estratégia atual (defaults = STRATEGY_WEIGHTS); reset defaults.
- **R4**: Fórmula documentada em technical-spec § scoring.
- **R5**: Testes: soma/clamp; pesos custom alteram ordenação de forma determinística.
- **Dependências:** Nenhuma
- **Desbloqueia / relacionada:** SPEC-020, SPEC-029
- **Fora de escopo:** ML de scoring, otimização automática de pesos.

## 3. Expectativas de UI/UX (se aplicável)
- **Há interface de usuário?** Sim
- Detalhamento fino na fase UX (fluxos, estados, microcopy, design-premises).
- Prioridade de produto: **P0**

### Definition of Done — UX
- [ ] Superfícies e estados (loading/empty/error/success) definidos
- [ ] Microcopy-chave (CTAs, erros)
- [ ] Alinhado a design-premises
- [ ] Aceite humano na fase UX

## 4. Checklist Técnico / Notas
- score_assets retorna breakdown em AssetAnalysis ou dict paralelo.
- Banco de dados: Não (salvo se Architect excepcionar)
- Novos pacotes: só se justificado na tech-spec
- Segurança: não persistir/logar API keys nem senha de IA

## 5. Definition of Ready (DoR)
- [x] Problema e valor claros (auditoria de melhorias)
- [x] Prioridade e dependências registradas
- [ ] Decisões finas de produto (se restarem) fechadas no chat PM antes do approve
- [x] Critérios de aceite testáveis nos requisitos

## 6. Definition of Done (DoD)
- [ ] Todos os requisitos da §2 atendidos
- [ ] Testes automatizados cobrem caminhos críticos
- [ ] `docs/CHANGELOG.md` + link em `docs/README.md` / backlog
- [ ] `./devkit review` APROVADO
- [ ] Tech-spec §9 se houver decisão arquitetural
