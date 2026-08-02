# Especificação de Feature: Observabilidade de runs (logging estruturado)

> **Prioridade:** P2 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** operador / desenvolvedor
- **Eu quero** logs com run_id, contagens e latências
- **Para que** diagnostique lentidão e falhas de ticker

## 2. Requisitos & Restrições
- **R1**: UUID/run_id por handle_generate_portfolio.
- **R2**: Logs: n tickers, ok, fail, ms fetch, ms score, ms IA.
- **R3**: LOG_LEVEL via env (INFO default).
- **R4**: Nunca logar API keys/senhas.
- **R5**: Teste unitário do formatter ou do contexto de run (sem assert de I/O pesado).
- **Dependências:** SPEC-018
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** OpenTelemetry/SaaS APM.

## 3. Expectativas de UI/UX (se aplicável)
- **Há interface de usuário?** Não — Opcional caption com run_id na UI
- Prioridade: **P2**

### Definition of Done — UX
- [x] N/A justificado

## 4. Checklist Técnico / Notas
- logging config module; app hooks.
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
