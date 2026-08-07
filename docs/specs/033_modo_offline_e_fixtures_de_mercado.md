# Especificação de Feature: Modo offline e fixtures de mercado

> **Prioridade:** P3 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** demo e CI
- **Eu quero** rodar app/demo sem rede
- **Para que** apresentações e testes estáveis sem Yahoo

## 2. Requisitos & Restrições
- **R1**: Flag OFFLINE_MODE env e/ou checkbox demo.
- **R2**: Fixtures JSON/parquet para conjunto mínimo de tickers (BR/US/cripto/BDR).
- **R3**: data_fetcher usa fixtures quando offline.
- **R4**: Documentar regeneração de fixtures; testes sem rede.
- **Dependências:** SPEC-025
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** Snapshot diário automático de mercado em CI paid.

## 3. Expectativas de UI/UX (se aplicável)
- **Há interface de usuário?** Sim
- Detalhamento fino na fase UX (fluxos, estados, microcopy, design-premises).
- Prioridade de produto: **P3**

### Definition of Done — UX
- [ ] Superfícies e estados (loading/empty/error/success) definidos
- [ ] Microcopy-chave (CTAs, erros)
- [ ] Alinhado a design-premises
- [ ] Aceite humano na fase UX

## 4. Checklist Técnico / Notas
- tests/fixtures/market/; fetcher switch.
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
