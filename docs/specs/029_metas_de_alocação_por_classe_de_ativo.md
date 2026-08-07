# Especificação de Feature: Metas de alocação por classe de ativo

> **Prioridade:** P3 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário com política de asset allocation
- **Eu quero** definir % alvo por classe (ações, FII, BDR, cripto, …)
- **Para que** a carteira respeite estratégia de longo prazo além do score unitário

## 2. Requisitos & Restrições
- **R1**: UI de metas por classe presentes no filtro; soma = 100% (validação).
- **R2**: Alocador combina score e metas (regra documentada no Architect — ex. waterfill por classe).
- **R3**: Feedback se meta inviável (classe sem candidatos).
- **R4**: Testes do alocador com metas.
- **Dependências:** SPEC-019, SPEC-016
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** Otimização convexa; constraints de setor.

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
- allocate_capital params; config defaults.
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
