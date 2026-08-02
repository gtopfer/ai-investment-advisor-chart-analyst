# Especificação de Feature: Onboarding DX: dotenv, README e empty CTAs

> **Prioridade:** P1 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** novo usuário e mantenedor
- **Eu quero** subir o app com menos fricção e mensagens acionáveis
- **Para que** configure env e saiba o que fazer em estados vazios

## 2. Requisitos & Restrições
- **R1**: Carregar `.env` no boot do app (python-dotenv) se o arquivo existir; não falhar se ausente.
- **R2**: README atualizado: BDRs, export CSV, threshold, prefs, classes, como testar.
- **R3**: Empty/error com CTA: limiar alto, zero tickers, failed_tickers, offline futuro.
- **R4**: Sem mudança de scoring/alocação.
- **R5**: requirements.txt inclui python-dotenv se adotado.
- **Dependências:** Nenhuma
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** Wizard de onboarding multi-página.

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
- app.py boot; ui empty helpers; docs.
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
