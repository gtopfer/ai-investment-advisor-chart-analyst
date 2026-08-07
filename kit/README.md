# jojo-ai — kit interno

Máquina do SPECKIT (agents, skills, scripts, templates).  

**Humanos não precisam abrir esta pasta no dia a dia.**  
Na raiz do projeto, edite só:

| Arquivo | Função |
| --- | --- |
| `../agents.md` | Produto + processo |
| `../system-design.md` | Arquitetura + design system |
| `../CHANGELOG.md` | Feito vs. pendente |

## Layout

```
kit/
├── docs/
│   ├── agents/          # runbooks
│   ├── skills/          # TDD, code-review, ui-ux, ducks
│   ├── recommendations.json
│   └── skill-validator.md
├── scripts/             # generate + validate
├── templates/           # scaffolding de specs
├── generated/           # registry + project-context (não editar)
├── meta/                # planos internos do kit
└── package.json
```

## Comandos (mantenedores / agentes)

```bash
cd kit
npm run sync
```

## Paths que agentes devem preferir

- Skills: `kit/docs/skills/*.md`
- Runbooks: `kit/docs/agents/*.md`
- Registry: `kit/generated/skills-registry.json`
- Context: `kit/generated/project-context.json`
- Recommendations: `kit/docs/recommendations.json`
