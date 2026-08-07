# Especificação de Feature: Histórico de runs na sessão

> **Prioridade:** P1 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário que itera parâmetros
- **Eu quero** revisitar gerações anteriores na mesma sessão
- **Para que** gerar de novo não apague o resultado anterior

## 2. Requisitos & Restrições
- **R1**: Manter N últimas runs em session_state (default N=5, configurável).
- **R2**: Seletor 'Histórico' para reexibir run (métricas, carteira, rebalance, export se 012).
- **R3**: Metadados: timestamp, estratégia, capital, threshold, n tickers.
- **R4**: Não persistir senhas/API keys no histórico.
- **R5**: Testes da estrutura de stack (push/limit).
- **Dependências:** Nenhuma
- **Desbloqueia / relacionada:** SPEC-022
- **Fora de escopo:** Histórico cross-session em servidor (conta).

## 3. Expectativas de UI/UX (se aplicável)
- **Há interface de usuário?** Sim
- Detalhamento fino na fase UX (fluxos, estados, microcopy, design-premises).
- Prioridade de produto: **P1**

### Definition of Done — UX
- [ ] Superfícies e estados (loading/empty/error/success) definidos
- [ ] Microcopy-chave (CTAs, erros)
- [ ] Alinhado a design-premises
- [ ] Aceite humano na fase UX

## 4. Checklist Técnico / Notas
- app last_run → run_history list.
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
