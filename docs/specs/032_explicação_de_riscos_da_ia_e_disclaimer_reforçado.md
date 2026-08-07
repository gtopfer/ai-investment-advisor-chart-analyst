# Especificação de Feature: Explicação de riscos da IA e disclaimer reforçado

> **Prioridade:** P3 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário leigo
- **Eu quero** entender limites da sugestão de IA e do app
- **Para que** eu não trate a saída como recomendação profissional

## 2. Requisitos & Restrições
- **R1**: Bloco de riscos/limites junto da análise IA (quando houver).
- **R2**: Disclaimer reforçado no fluxo de resultados (além do rodapé).
- **R3**: Microcopy PT revisada (skill microcopy); sem jargão excessivo.
- **R4**: Não altera scoring nem prompts além de eventualmente pedir bullets de risco se barato.
- **Dependências:** Nenhuma
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** Compliance jurídico formal; parecer de advogado.

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
- ui copy; optional AI prompt field risks.
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
