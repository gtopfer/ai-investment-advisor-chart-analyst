---
name: Autonomous Loop
type: development
category: quality
description: Self-heal loop with max 3 attempts per root cause after review failures
usedFor: [code, fix, review]
appliesTo: [backend, frontend]
requiredKnowledge: [debugging, testing]
conflicts: []
---

# Skill: Loop Autônomo e Autocorreção

> **Usado por**: Developer em `test_red` (e qualquer agente que corrija falhas de `./jojo review`).  
> **Objetivo**: maximizar progresso com feedback real, sem loop infinito de tokens.

## Quando usar

- Após escrever ou alterar código.  
- Quando `./jojo review` ou a suíte de testes falha.  
- Depois de um `reject` que devolveu a spec a `test_red`.

## Quando NÃO usar

- Em fases sem implementação (draft, UX, architect puro).  
- Para inventar requisitos ou expandir escopo.  
- Quando a falha é de infraestrutura externa (escalar ao humano de imediato).

## O ciclo (ordem fixa)

```
1. PLANEJAR    → o que deve mudar? quais arquivos? qual teste prova?
2. ESCREVER    → menor mudança correta
3. EXECUTAR    → ./jojo review  (e runner da stack se o review não cobrir tudo)
4. AVALIAR     → APROVADO? avança. REPROVADO? classifique a falha
5. CORRIGIR    → uma causa raiz por vez
6. (opcional) REFATORAR → só com verde; re-rode o review
```

Nunca pule **EXECUTAR**. “Compila na minha cabeça” não conta.

## Classificação da falha (AVALIAR)

| Tipo | Sinais | Resposta |
|------|--------|----------|
| **Sintaxe / lint** | parse error, ruff/eslint | Corrija o arquivo indicado |
| **Tipo / build** | tsc, mypy, cargo | Ajuste tipos/assinaturas; não cale o typechecker |
| **Teste (assert)** | expected ≠ actual | Corrija produção **ou** teste se o teste estiver errado vs spec |
| **Teste (setup)** | mock, fixture, import | Conserte o harness sem enfraquecer o assert |
| **TODO/FIXME** | review flagrou comentário | Remova e complete o comportamento |
| **Infra** | porta, credencial, DB down | **Não** tente 3x a mesma config — escale |
| **Escopo** | falta requisito/lib | Pare e pergunte ao humano |

## Autocorreção (self-healing)

1. Leia a **primeira** falha relevante do log (não a última de uma cascata se possível).  
2. Identifique **um** arquivo e **uma** causa.  
3. Aplique o patch mínimo.  
4. Rode `./jojo review` de novo.  
5. Se a mesma causa falhar de novo, registre tentativa #N e mude a hipótese — não repita o mesmo patch.

### Contador de tentativas

- Conta **por causa raiz** (mesmo erro essencial), não por qualquer falha diferente.  
- **Limite: 3**. Na 4ª ocorrência da mesma causa → **STOP**.

## Condições de parada (escalar ao humano)

Pare o loop e peça ajuda se:

1. 3 tentativas na mesma causa raiz falharam.  
2. A correção exige dependência/pacote **não** previsto na spec/tech-spec.  
3. Infraestrutura externa impede o teste (credencial, serviço, permissão de OS).  
4. A tech-spec/contratos estão contraditórios ou incompletos.  
5. O usuário mudou a spec no meio do ciclo (chame o Squad Lead).

### Formato de escalação

```text
[Autonomous Loop] STOP — precisa de decisão humana
Causa raiz: ...
Tentativas:
1. ... → erro
2. ... → erro
3. ... → erro
Logs (trecho):
...
Pergunta / decisão necessária:
...
```

## Depois do verde

1. Refatore se o código ficou feio **sem** mudar comportamento.  
2. Rode `./jojo review` outra vez.  
3. Passe pelo checklist de `kit/docs/skills/code-review.md`.  
4. Só então `./jojo approve`.

## Anti-padrões

| Evite | Por quê |
|-------|---------|
| Mudar 10 arquivos a cada falha | Difícil isolar causa |
| Comentar testes | Esconde regressão |
| Ampliar escopo no meio do loop | Nunca fica verde |
| Rodar review só no final de 1h de edits | Feedback tarde demais |
| Ignorar a 1ª falha e caçar a 12ª | Cascata |

## Ligação com o kit

```
fail(review) → classificar → patch → review → ...
     └─ 3x mesma causa → STOP → humano
     └─ verde → code-review skill → approve
```
