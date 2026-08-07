# Especificação de Feature: i18n inglês da interface

> **Prioridade:** P3 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário anglófono
- **Eu quero** UI em inglês
- **Para que** audiência internacional use o app

## 2. Requisitos & Restrições
- **R1**: Seletor PT | EN (default PT).
- **R2**: Strings principais de UI externalizadas (dict ou gettext simples).
- **R3**: Disclaimer, empty states, labels de tabelas traduzidos.
- **R4**: Teste: idioma default PT; chave EN existe para strings críticas.
- **Dependências:** SPEC-024
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** ES/outros idiomas; RTL.

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
- ui/i18n.py; preferência persistida se 022.
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
