# CHANGELOG

Rastreamento do projeto (o que foi feito vs o que falta).  
Atualizado por agentes com aceite humano. **Fica na raiz** junto com `agents.md` e `system-design.md`.

## [Unreleased]

### Implemented
- [x] jojo-ai v1.4 instalado: `agents.md` (Features), `system-design.md`, `CHANGELOG.md`, `kit/`
- [x] CI `jojo-review.yml` (`cd kit && npm run sync`)
- [x] Seção 1 + Features preenchidas com histórico do app (001–035 entregues)
- [x] `system-design.md` com arquitetura e design system do app
- [x] Kit sincronizado a partir do repositório jojo-ai de referência
- [x] DevKit removido (sem `./devkit`, hooks ou CI legada)
- [x] Auditoria Features vs código (2026-08-07): 36 itens revalidados `[x]`; pytest OK
- [x] Ducks Pattern: código em `ducks/*` + `shared/*`, APIs públicas, docs/system-design alinhados
- [x] Design system monocromático: `docs/design-system.md`, tokens nomeados em `ducks/ui/theme.py`, §3 atualizado

### To Do (Validated by Human)
- [ ] Próxima feature: adicionar `- [ ] …` em `agents.md` → Features
