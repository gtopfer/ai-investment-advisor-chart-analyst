---
name: TDD
type: development
category: quality
description: Test-Driven Development — RED → GREEN → REFACTOR cycle
usedFor: [code, tests, refactor]
appliesTo: [backend, frontend]
requiredKnowledge: [testing-frameworks, assertions]
conflicts: [skip-tests, no-tests]
---

# Skill: TDD (Test-Driven Development)

> **Usado por**: QA (fase `tech_approved`) e Developer (respeita RED→GREEN→REFACTOR).  
> **Comando de verdade do kit**: a suíte local + `./jojo review` no fechamento.

## Quando usar

- Sempre que uma feature/refatoração entra em `tech_approved` ou o harness precisa ser ampliado.
- Nunca “testar depois se der tempo”.

## Quando NÃO usar

- Documentação pura sem comportamento observável.
- Spike exploratório explicitamente fora de produção (ainda assim: anote dívida e volte com RED).

## Fontes da verdade (nesta ordem)

1. **Spec ativa** — `.ai/specs/<nome>.md` (requisitos, restrições, DoD)  
2. **Gherkin** — `.ai/features.feature` ou `.feature` dedicado  
3. **Contratos** — `.ai/technical-spec.md` §5  
4. **Modelo** — `.ai/template.specs` só para estrutura de seções, **não** para inventar requisitos  

## Ciclo

```
RED     → escreva um teste que falha pelo motivo certo (comportamento ausente)
GREEN   → implemente o mínimo para passar
REFACTOR→ limpe sem mudar comportamento; mantenha verde
```

Repita por fatia vertical (um cenário/requisito por vez). Não escreva a suíte inteira e depois o sistema inteiro se a fatia for grande demais para feedback rápido — mas na fase QA do jojo-ai a suíte RED completa da feature é o entregável antes do Dev.

## Derivação (checklist)

| Origem | Testes mínimos |
|--------|----------------|
| Cenário Gherkin | ≥ 1 teste automatizado |
| Requisito de negócio | 1 positivo + 1 negativo |
| Validação de entrada | 1 sucesso + 1 por tipo de falha relevante |
| Borda na spec | 1 teste explícito |
| Erro de integração (contrato) | 1 teste com mock do falha |

## Anatomia do teste

```
Arrange  — dados, mocks, estado inicial
Act      — uma ação principal
Assert   — comportamento observável (não detalhe privado)
```

### Nomes

- Bom: `rejeita email vazio`, `lista apenas itens do usuário autenticado`  
- Ruim: `test1`, `funciona`, `chama validateEmail`

### Isolamento

- Mock: BD, HTTP, FS, clock, random, auth externa  
- Unitário **não** sobe servidor real nem toca rede  
- Um arquivo de teste ≈ uma unidade (função, use case, componente)

### Layout

Espelhe o código: `src/domain/pricing.ts` → `tests/domain/pricing.spec.ts` (ou convenção da stack).

## Prova de RED (obrigatória na fase QA)

Antes de `./jojo approve` em `tech_approved`:

1. Rode a suíte.  
2. Novos testes **falham**.  
3. A mensagem de falha aponta comportamento ausente, não `SyntaxError` no teste.  
4. Se já passam: asserts estão frouxos ou a implementação já existia — ajuste.

## Prova de GREEN (fase Developer)

- Todos os testes da feature passam.  
- Não delete asserts.  
- `skip`/`xit` só com justificativa no chat e acordo do PM.

## Anti-padrões

| Evite | Faça |
|-------|------|
| Testar implementação privada | Testar contrato/comportamento |
| Um mega-teste de 200 linhas | Vários casos focados |
| Snapshots frágeis como único assert | Asserts semânticos |
| Dependência de ordem entre testes | Cada teste independente |
| Dados mágicos sem nome | Fixtures/builders legíveis |

## Critérios de saída (feature)

- [ ] Todo cenário `.feature` relevante tem teste  
- [ ] Requisitos da §2 cobertos (pos/neg/borda)  
- [ ] Mocks nas bordas externas  
- [ ] Suíte executável na CI/local do projeto  
- [ ] Em GREEN: zero falhas; code-review skill aplicada no fechamento  

## Ligação com o kit

```
QA (RED)  --approve--> Developer (GREEN) --review+approve--> QA (validação)
         tdd.md              tdd + autonomous-loop + code-review
```
