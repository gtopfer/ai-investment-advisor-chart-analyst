# Skill Validator Checklist

> **Quem usa:** mantenedores do kit e agentes que propõem skills novas.  
> **Quem NÃO usa:** o usuário final do SPECKIT — ele só edita `agents.md`.

Rode:

```bash
npm run validate:skills
# ou
node scripts/validate-skills.js docs/skills/minha-skill.md
```

## Checklist obrigatório

- [ ] Frontmatter YAML válido no topo (`---` … `---`)
- [ ] Campos: `name`, `type`, `category`, `description`
- [ ] `description` &lt; 1024 chars
- [ ] Seção **Quando usar**
- [ ] Seção **Quando NÃO usar** (evita overlap)
- [ ] Exemplos ou checklist práticos
- [ ] Sem HTML solto fora de code fences
- [ ] Após merge: `npm run generate:registry`

## Campos recomendados

| Campo | Exemplo |
| --- | --- |
| `usedFor` | `[code, tests]` |
| `appliesTo` | `[backend, frontend]` |
| `requiredKnowledge` | `[jest, typescript]` |
| `conflicts` | `[skip-tests]` |
| `mandatory` | `true` (só guardrails do kit) |

## Types & categories padrão

**type:** `development` · `design` · `architecture` · `documentation` · `knowledge` · `refinement`  
**category:** `quality` · `design` · `organization` · `documentation` · `knowledge` · `infra`

## Superfície do usuário

Skills novas **não** criam configuração para o humano.  
O único arquivo de setup do projeto continua sendo **`agents.md`**.
