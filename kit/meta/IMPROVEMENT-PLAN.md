# Plano de Melhoria — jojo-ai

**Status:** Tier 1–4 implementados com **UX single-file**.

---

## Guardrail de produto (inviolável)

```
User-facing config surface = agents.md (Seção 1) + system-design.md only.
```

| Arquivo | Responsabilidade |
| --- | --- |
| `agents.md` | Produto, processo, guardrails |
| `system-design.md` | Arquitetura + design system **deste** projeto |

Qualquer artefato extra é:

- **gerado** a partir de `agents.md` (`project-context.json`), ou
- **interno do kit** (skills, registry, recommendations, validators), ou
- **produzido por agentes** com aceite humano (specs, código, CHANGELOG).

Nunca: pedir ao usuário `stack.md`, `guardrails.md`, `design-premises.md`, `agents-profile.md` separados — isso vive nos 2 arquivos acima.  
Agentes e skills **devem ler `system-design.md`** antes de designar arquitetura ou UI.

---

## Implementado

### Tier 1 — Estrutura de skills

- [x] Frontmatter YAML em `kit/docs/skills/*`
- [x] Types/categories (`development`, `design`, `architecture`, …)
- [x] `kit/scripts/generate-registry.js` → `skills-registry.json`
- [x] `npm run generate:registry`

### Tier 2 — Qualidade

- [x] `docs/skill-validator.md` + `kit/scripts/validate-skills.js`
- [x] `requiredKnowledge`, `appliesTo`, `conflicts` no frontmatter
- [x] Seções **Quando usar** / **Quando NÃO usar** nas skills
- [x] `npm run validate:skills`

### Tier 3 — Project context + system design

- [x] `kit/scripts/generate-context.js` lê **Seção 1 de agents.md**
- [x] Emite `project-context.json` (stack, users, guardrails + pointer `system-design.md`)
- [x] **`system-design.md`** dedicado por projeto (arquitetura §2 + design system §3)
- [x] Agents/skills apontam para `system-design.md` (não guidelines soltas)
- [x] `npm run generate:context`

### Tier 4 — Discovery (defaults do kit)

- [x] `docs/recommendations.json` — skills por contexto e por fase
- [x] Registry + recommendations para agentes
- [x] Sem `agents-profile.md` de config humana

### DX

- [x] `package.json` com `sync` / `test:scripts`
- [x] Princípio documentado em `agents.md` e `README.md`

---

## Como agentes usam (sem envolver o usuário)

```bash
npm run sync
```

1. Valida skills  
2. Regenera `skills-registry.json`  
3. Regenera `project-context.json` a partir de `agents.md`

---

## Próximos (opcional, sem quebrar UX)

- [ ] CLI `./jojo` (status/approve/review) lendo o mesmo `agents.md`
- [ ] CI workflow rodando `npm run sync` no meta-repo
- [ ] Agente, no bootstrap, oferecer preencher Seção 1 via entrevista (ainda grava só em `agents.md`)

---

## Filosofia

```
SPECKIT single-file
    + metadados de skills (só kit)
    + validação (só kit)
    + context JSON (derivado de agents.md)
    + recommendations (defaults)
    = discovery para agentes, zero config extra para humanos
```
