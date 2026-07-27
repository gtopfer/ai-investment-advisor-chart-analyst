# Skills de engenharia

Procedimentos reutilizáveis invocados pelos agents. Não são fases — são **como** executar partes do trabalho.

| Skill | Arquivo | Quem usa | Quando |
|-------|---------|----------|--------|
| UI/UX | [`ui-ux.md`](ui-ux.md) | UX Designer; Dev/QA com UI | Fase `spec_approved`; implementação visual |
| Microcopy | [`microcopy.md`](microcopy.md) | UX, PM, Developer | Textos de UI (CTA, erro, empty) |
| TDD | [`tdd.md`](tdd.md) | QA (RED), Developer (GREEN) | `tech_approved` e implementação |
| Code review | [`code-review.md`](code-review.md) | Developer, QA validação | Antes de `approve` em `test_red` / `code_review` |
| Loop autônomo | [`autonomous-loop.md`](autonomous-loop.md) | Developer | Falhas de build/teste/`./devkit review` |

Orquestração: [`.ai/agents/squad-lead.agent.md`](../agents/squad-lead.agent.md).
