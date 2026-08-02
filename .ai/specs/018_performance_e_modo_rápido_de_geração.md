# Especificação de Feature: Performance e modo rápido de geração

> **Prioridade:** P0 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário gerando carteira com muitas classes/tickers
- **Eu quero** geração mais estável, com progresso e opção rápida
- **Para que** eu saiba o andamento e reduza rate-limit/timeout do Yahoo

## 2. Requisitos & Restrições
- **R1**: max_workers de fetch configurável (env + default ≤ 5; hoje 10).
- **R2**: Progresso por fase na UI: coleta → indicadores → IA (se houver).
- **R3**: Modo rápido (checkbox): desliga IA e pode pular passos pesados documentados (ex. dividend history detalhado se Architect validar).
- **R4**: Backoff/retry no data_fetcher permanece ou melhora; documentar limites.
- **R5**: Testes: workers default; modo rápido não chama IA (mock).
- **Dependências:** SPEC-017
- **Desbloqueia / relacionada:** SPEC-020, SPEC-027, SPEC-033
- **Fora de escopo:** Fila distribuída, múltiplos providers de market data.

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
- app.analyze_assets; config FETCH_MAX_WORKERS; UI avançado.
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
