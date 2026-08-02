# Especificação de Feature: Custos de corretagem e IR simplificado no rebalance

> **Prioridade:** P3 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário BR avaliando se rebalance vale a pena
- **Eu quero** estimar corretagem e IR simplificado no plano
- **Para que** eu veja custo vs benefício do ajuste

## 2. Requisitos & Restrições
- **R1**: Parâmetros educacionais: % corretagem e alíquota IR simplificada (defaults documentados).
- **R2**: Resumo de custo estimado no plano de rebalance (+ opcional por linha).
- **R3**: Disclaimer: não é cálculo fiscal oficial nem aconselhamento.
- **R4**: Testes das fórmulas com casos fixos.
- **Dependências:** SPEC-016
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** Integração corretora real; DARF; come-cotas FII completo.

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
- allocator cost helper; UI rebalance.
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
