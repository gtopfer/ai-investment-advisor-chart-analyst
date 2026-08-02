# Especificação de Feature: Comparar estratégias lado a lado

> **Prioridade:** P1 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário indeciso entre Growth / Dividendos / Equilíbrio
- **Eu quero** comparar alocações sem reconfigurar tudo
- **Para que** eu escolha estratégia com a mesma carteira e capital

## 2. Requisitos & Restrições
- **R1**: Ação 'Comparar estratégias' gera visão para ≥2 estratégias (todas as 3 no MVP se barato).
- **R2**: Reutilizar análise de ativos já coletada (só re-score/allocate).
- **R3**: UI: tabela/cards com top alocações e overlap de tickers.
- **R4**: Não exige novo fetch se last_run/scored base existir; senão gera uma vez e compara.
- **R5**: Testes do comparador com assets mock.
- **Dependências:** SPEC-018, SPEC-019
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** Otimização multi-objetivo; Pareto completo.

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
- allocator compare helper; UI results.
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
