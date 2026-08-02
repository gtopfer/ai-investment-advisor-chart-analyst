# Especificação de Feature: Persistência robusta de preferências

> **Prioridade:** P1 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário recorrente
- **Eu quero** salvar carteira/prefs sem URL longa e sem vazar ao compartilhar link
- **Para que** reload e privacidade funcionem melhor que só query params

## 2. Requisitos & Restrições
- **R1**: Backend de storage: localStorage (component Streamlit) **e/ou** arquivo local single-user; Architect escolhe com trade-off.
- **R2**: Migrar token `prefs` da URL se existir (SPEC-013).
- **R3**: Manter Salvar / Limpar; nunca persistir AI_ACCESS_PASSWORD nem API keys.
- **R4**: Query params deixam de ser o primary store (podem ficar como share opcional).
- **R5**: Testes de codec/migração; smoke de clear.
- **Dependências:** SPEC-013
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** Conta cloud multi-dispositivo.

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
- portfolio/persistence.py evolution; possível dep streamlit-js-eval ou equivalente leve.
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
