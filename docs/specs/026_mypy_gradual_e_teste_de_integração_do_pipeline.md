# Especificação de Feature: Mypy gradual e teste de integração do pipeline

> **Prioridade:** P2 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** desenvolvedor / QA
- **Eu quero** typecheck de domínio + um teste ponta a ponta mockado
- **Para que** regressões de contrato e pipeline sejam detectadas cedo

## 2. Requisitos & Restrições
- **R1**: mypy em models/, portfolio/, allocator/ (gradual; configs em pyproject/mypy.ini).
- **R2**: Teste integração: process_portfolio com market data mockado cobre threshold + short_history path.
- **R3**: Documentar no README; idealmente `./devkit review` roda mypy se configurado.
- **R4**: CI workflow pode invocar pytest+mypy.
- **Dependências:** SPEC-025
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** strict mypy em 100% do repo na primeira PR.

## 3. Expectativas de UI/UX (se aplicável)
- **Há interface de usuário?** Não — Tooling
- Prioridade: **P2**

### Definition of Done — UX
- [x] N/A justificado

## 4. Checklist Técnico / Notas
- dev deps mypy; tests/test_pipeline_integration.py.
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
