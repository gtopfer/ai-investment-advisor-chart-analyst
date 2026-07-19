# Skill: Test-Driven Development (TDD — Desenvolvimento Orientado a Testes)

Gere os testes ANTES da implementação, derivados diretamente dos critérios de aceitação em `.ai/template.specs` e dos cenários no arquivo `.feature` correspondente. Agnóstico de linguagem — troque os nomes de ferramenta pela stack real do projeto.

## Ciclo

```
1. RED    (vermelho)  — escreva um teste que falha para um cenário Gherkin ou requisito
2. GREEN  (verde)     — escreva o mínimo de código para fazê-lo passar
3. REFACTOR (refatorar) — limpe sem mudar o comportamento; os testes continuam verdes
```

## Regras de Derivação
1. Todo cenário Given/When/Then (Dado/Quando/Então) no arquivo `.feature` → pelo menos um teste
2. Toda regra de negócio na spec → um teste positivo + um teste negativo
3. Toda validação → um teste de sucesso + um teste por caso de falha
4. Casos de borda citados em "Requisitos e Restrições" → testes explícitos, não cobertura presumida

## Estrutura

```
describe("[Feature]")
  describe("[Cenário / critério de aceitação]")
    it("deve [comportamento esperado]")
      // Arrange (organizar)
      // Act (agir)
      // Assert (verificar)
```
(Adapte ao framework de teste do projeto — `describe/it` do Vitest/Jest, classes/funções do pytest, testes de tabela do Go, etc. O formato Arrange/Act/Assert se mantém.)

## Convenções
- Mocke todas as dependências externas (BD, rede, sistema de arquivos, auth) em testes unitários — nunca acesse serviços reais
- Um arquivo de teste foca em uma única unidade (uma função, um módulo, um endpoint)
- Nomes de teste descrevem comportamento, não implementação ("rejeita título vazio", não "chama validate()")
- Espelhe a estrutura do código-fonte no diretório de testes (`src/foo/bar.ts` → `tests/foo/bar.spec.ts`)

## Critérios de Saída (antes de considerar a feature pronta)
- [ ] Todo cenário do arquivo `.feature` tem um teste passando
- [ ] Todo caso negativo/de borda na spec tem um teste passando
- [ ] Suíte completa passa — zero falhas, zero testes pulados sem justificativa
- [ ] O checklist de `.ai/skills/code-review.md` foi executado nos arquivos alterados
