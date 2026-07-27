# Agents (runbooks)

Cada agent é o procedimento operacional de um papel na máquina de estados. O **Squad Lead** escolhe qual carregar com base em `.ai/state.md`.

| Agent | Arquivo | Status | Papel |
|-------|---------|--------|-------|
| Squad Lead | [`squad-lead.agent.md`](squad-lead.agent.md) | (sempre) | Sync, escolhe fase, proíbe pular etapas |
| Product Manager | [`product-manager.agent.md`](product-manager.agent.md) | `draft`, `tested` | Spec de negócio + DoD |
| UX / UI Designer | [`ux-designer.agent.md`](ux-designer.agent.md) | `spec_approved` | Fluxos, estados, design system |
| Architect | [`architect.agent.md`](architect.agent.md) | `ux_approved` | Tech-spec, stack, contratos |
| QA | [`qa.agent.md`](qa.agent.md) | `tech_approved`, `code_review` | TDD RED + validação GREEN |
| Developer | [`developer.agent.md`](developer.agent.md) | `test_red` | Implementação + review |

Fluxo: **PM → UX → Architect → QA → Developer → QA → PM**.

Todos seguem: **entradas → processo → gate de approve/reject → anti-padrões → handoff**.

Skills: [`.ai/skills/`](../skills/).
