# Especificação de Feature: Fatiar UI em módulos (sidebar, results, theme)

> **Prioridade:** P2 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** desenvolvedor mantenedor
- **Eu quero** módulos de UI por responsabilidade
- **Para que** features de interface sejam mais fáceis de revisar

## 2. Requisitos & Restrições
- **R1**: Extrair `ui/theme.py`, `ui/sidebar.py`, `ui/results.py` (nomes finais no Architect).
- **R2**: layout.py vira fachada ou some; app.py só orquestra.
- **R3**: Nenhuma regressão visual/fluxo; testes verdes.
- **R4**: Atualizar architecture-guidelines e README árvore.
- **Dependências:** Nenhuma
- **Desbloqueia / relacionada:** SPEC-031, SPEC-035
- **Fora de escopo:** Design system completo multi-página Streamlit multipage.

## 3. Expectativas de UI/UX (se aplicável)
- **Há interface de usuário?** Não — Refactor interno; comportamento visual inalterado
- Prioridade: **P2**

### Definition of Done — UX
- [x] N/A justificado

## 4. Checklist Técnico / Notas
- move only; no behavior change.
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
