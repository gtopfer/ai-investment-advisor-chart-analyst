# Parallelization — Multiple Agents Working Together

Como múltiplos agentes trabalham em paralelo, coordenados apenas por `agents.md`.

---

## 🎯 Princípio

**agents.md é a régua única e a única config humana do SPECKIT.**  
Não há cronograma, não há fases de tempo. Apenas:

- Humanos editam **só** `agents.md` (Seção 1)
- Agentes lêem agents.md (+ registry/context gerados)
- Agentes trabalham em seus domínios
- Agentes sincronizam quando necessário
- **Nunca** peça ao usuário novos arquivos de config

---

## 👥 Agentes & Domínios

```
Agent-Skills
├─ Responsável por: kit/docs/skills/, kit/scripts/generate-registry.js
├─ Lê: agents.md + IMPROVEMENT-PLAN.md (Tier 1)
└─ Trabalha em paralelo: Sim (domínio isolado)

Agent-Context
├─ Responsável por: .ai/guidelines/, kit/scripts/generate-context.js
├─ Lê: agents.md + IMPROVEMENT-PLAN.md (Tier 3)
└─ Trabalha em paralelo: Sim (domínio isolado)

Agent-Discovery
├─ Responsável por: kit/docs/agents/, kit/scripts/recommendation-*.js
├─ Lê: agents.md + IMPROVEMENT-PLAN.md (Tier 4)
└─ Trabalha em paralelo: Sim (domínio isolado)

Agent-Testing
├─ Responsável por: tests/, kit/scripts/validate-*.js
├─ Lê: agents.md + IMPROVEMENT-PLAN.md (todos os tiers)
└─ Trabalha em paralelo: Sim (testa tudo)

Agent-Docs
├─ Responsável por: agents.md, README.md, templates/
├─ Lê: agents.md + IMPROVEMENT-PLAN.md (visão geral)
└─ Trabalha em paralelo: Sim (docs separadas)

Agent-Review
├─ Responsável por: Code review, merge gate
├─ Lê: agents.md + Pull requests
└─ Trabalha em paralelo: Sim (continuous review)
```

---

## 🔄 Fluxo de Trabalho (Sem Timeline)

```
Agent começa
  ↓
Lê agents.md (régua)
  ↓
Lê IMPROVEMENT-PLAN.md (o que fazer)
  ↓
Identifica seu domínio
  ↓
Cria branch: git checkout -b feat/seu-dominio
  ↓
Trabalha (commits frequentes)
  ↓
Daily: git push origin feat/seu-dominio
  ↓
Quando pronto: Abre PR
  ↓
Agent-Review: Valida qualidade
  ↓
Se OK: Merge → main
  ↓
Se não OK: Volta para trabalhar
```

---

## 🛡️ Parallelização por Isolamento de Domínio

### Sem Conflitos

```
Agent-Skills edita:        kit/docs/skills/*, kit/scripts/generate-registry.js
Agent-Context edita:       .ai/guidelines/*, kit/scripts/generate-context.js
Agent-Discovery edita:     kit/docs/agents/*, kit/scripts/recommendation-*.js
Agent-Testing edita:       tests/*, kit/scripts/validate-*.js
Agent-Docs edita:          agents.md, README.md, templates/
Agent-Review:              Reviews (não edita exceto merge)

✓ Zero overlaps = Nenhum merge conflict
✓ Múltiplos agentes podem trabalhar ao mesmo tempo
```

### Conflito Possível

Se 2+ agentes editarem `agents.md` simultâneamente:
- **Solução:** Agent-Docs é responsável por agents.md
- **Outros:** Só sugerem mudanças via issue/PR comment
- **Merge:** Agent-Review coordena final merge

---

## ✅ Quality Gates (Toda PR)

Antes de merge → main:

```
✓ npm run lint       (Sem erros de style)
✓ npm run test       (Testes passam)
✓ npm run validate   (Validadores passam)
✓ Sem TODOs/FIXMEs   (Código completo)
✓ Docs atualizadas   (Se necessário)
✓ Code review OK     (Agent-Review aprova)
```

---

## 🔀 Git Strategy (Simples)

```
main (production)
├── feat/tier1-skills (Agent-Skills)
├── feat/tier3-context (Agent-Context)
├── feat/tier4-discovery (Agent-Discovery)
├── feat/testing (Agent-Testing)
└── feat/docs (Agent-Docs)

Workflow:
1. Agent: git checkout -b feat/seu-dominio
2. Agent: Trabalha + commits
3. Agent: git push origin feat/seu-dominio
4. Agent: Abre PR quando pronto
5. Agent-Review: Valida
6. Se OK: git merge feat/seu-dominio → main
7. If not: Volta para step 2
```

---

## 📌 Sincronização (Sem Cronograma)

Agentes sincronizam quando:

1. **PR pronto:** "Abrindo PR para review"
2. **Bloqueado:** "Preciso de X do outro agente antes de continuar"
3. **Merge conflict:** Coordenam via Slack/chat
4. **Integration test:** "Posso testar tudo junto?"

---

## 🚀 Como Começar

Cada agente:

```bash
# 1. Ler agents.md
cat agents.md

# 2. Ler IMPROVEMENT-PLAN.md
cat IMPROVEMENT-PLAN.md

# 3. Escolher seu Tier
# Agent-Skills: Tier 1
# Agent-Context: Tier 3
# Agent-Discovery: Tier 4
# Agent-Testing: Todos
# Agent-Docs: Todos

# 4. Criar branch
git checkout -b feat/seu-dominio

# 5. Trabalhar
# (edite arquivos do seu domínio)

# 6. Commit
git add .
git commit -m "feat(seu-tier): descrição"

# 7. Push
git push origin feat/seu-dominio

# 8. Quando pronto: Abrir PR
# (diga em Slack quando PR está pronto)

# 9. Aguardar review
# Agent-Review valida

# 10. Se OK: Merge (Agent-Review faz)
# Se não: Volte ao passo 5
```

---

## 📋 Domains (Responsabilidades Claras)

### Agent-Skills: Tier 1 - Skills Metadata

**Edita:**
- `kit/docs/skills/*.md` — Add YAML frontmatter
- `kit/scripts/generate-registry.js` — Create registry generator
- `docs/skill-types.json` — Define types/categories

**Não edita:** Nenhum outro arquivo

**Quando termina:** Abre PR, diz "Tier 1 Skills pronto"

---

### Agent-Context: Tier 3 - Project Context

**Edita:**
- `.ai/guidelines/` — Define stack, conventions, guardrails schemas
- `kit/scripts/generate-context.js` — Create context generator
- `schemas/project-context.json` — JSON schema

**Não edita:** Nenhum outro arquivo

**Quando termina:** Abre PR, diz "Tier 3 Context pronto"

---

### Agent-Discovery: Tier 4 - Agent Discovery

**Edita:**
- `kit/docs/agents/` — Agent profiler, definitions
- `kit/scripts/recommendation-engine.js` — Recommendation logic
- Integração com skills + context

**Não edita:** Nenhum outro arquivo

**Quando termina:** Abre PR, diz "Tier 4 Discovery pronto"

---

### Agent-Testing: All Tiers - Quality Gates

**Edita:**
- `tests/` — Test files
- `kit/scripts/validate-*.js` — Validators
- `.github/workflows/` — CI/CD

**Testa:** Output de todos os outros agentes

**Quando termina:** Abre PR, diz "Tests for Tiers X, Y, Z ready"

---

### Agent-Docs: All Tiers - Documentation

**Edita:**
- `agents.md` — Update based on changes
- `README.md` — Keep in sync
- `templates/` — Update examples
- `docs/` guides — Create quality guides

**Coordena:** Final merge de docs ao main

**Quando termina:** Abre PR, diz "Docs updated"

---

### Agent-Review: All PRs - Quality Gate

**Não edita arquivos.**

**Faz:**
- Code review toda PR
- Valida quality gates
- Aprova ou pede mudanças
- Faz merge para main quando OK

**Comunica:** "PR X aprovada, merging" ou "PR X precisa de ajustes em Y"

---

## 🎯 Resumo

**agents.md é tudo que importa:**
- Define 8 fases (draft → done)
- Define 6 agentes
- Define 3 skills

**IMPROVEMENT-PLAN.md é o que fazer:**
- Tier 1: Metadados
- Tier 2: Validação
- Tier 3: Context
- Tier 4: Discovery

**Agentes trabalham em paralelo:**
- Cada um em seu domínio
- Sincronização apenas quando necessário
- Sem cronograma artificial
- Qualidade garantida por gates

---

**Status:** Simples. Claro. Agnóstico. Pronto.
