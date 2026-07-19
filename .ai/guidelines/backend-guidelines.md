# Guia de Backend

Padrões de implementação para a camada de backend: use cases, pontos de entrada, persistência, autenticação, variáveis de ambiente, testes.

> Stack e estrutura de camadas: ver `architecture-guidelines.md`.

---

## Use Cases

- Um use case = uma função/classe, um arquivo
- Nome do arquivo: `kebab-case` (ex.: `create-ticket.ts` / `create_ticket.py`)
- Estrutura interna: validar entrada → checar acesso → executar a operação
- Nunca leia estado de auth/sessão dentro de um use case — isso é trabalho do adapter

### Injeção de Dependências

Quando um use case precisa de dependências externas (BD, APIs, sistema de arquivos), injete-as como parâmetros via interfaces:

```typescript
// Bom — testável, dependências injetadas como interfaces
async function processBatch(
  options: BatchOptions,
  deps: { reader: CsvReader; client: ApiClient; writer: ResultWriter }
): Promise<void> { /* ... */ }

// Ruim — difícil de testar, import direto acopla à implementação
import { CsvReader } from "@/infra/csv/csv-reader"
async function processBatch(options: BatchOptions): Promise<void> {
  const reader = new CsvReader() // não dá pra mockar sem mockar o módulo inteiro
}
```

Isso permite que o QA escreva testes unitários com mocks simples, em vez de mockar módulos inteiros.

---

## Pontos de Entrada (Adapters)

A camada de adapters (controllers HTTP, server actions, comandos CLI) é onde as requisições entram no sistema — equivalente a controllers em arquiteturas REST.

- Autentique/autorize antes de qualquer operação
- Delegue a lógica de negócio ao use case — sem lógica de negócio no adapter
- Valide a entrada contra um schema antes de chamar o use case
- Retorne resultados tipados (`{ success, error }`) — não deixe exceções cruas vazarem pro chamador
- Dispare qualquer invalidação de cache/revalidação de UI necessária após mutações

---

## Persistência

- **Exclusão lógica (soft delete)** — entidades principais ganham um campo de timestamp `deletedAt`/`deleted_at`; evite exclusão física (hard delete) sem justificativa documentada
- **UUID como ID** — prefira UUIDs a auto-incremento para entidades de domínio
- **Migrations obrigatórias** — mudanças de schema passam pela ferramenta de migração do projeto; nunca aplique mudanças de schema direto num ambiente compartilhado

---

## Autenticação

- Todo ponto de entrada que toca dados do usuário verifica a sessão como **primeira operação**
- Nunca confie num ID de usuário/tenant vindo do cliente — sempre derive da sessão verificada
- Nunca exponha tokens de sessão ou segredos ao cliente

---

## Variáveis de Ambiente

- Nenhum valor fixo no código (hardcoded) para nada sensível ou específico de ambiente
- Extraia para variáveis de ambiente: URLs, chaves de API, credenciais, portas, segredos
- Mantenha o `.env.example` atualizado com toda variável que o projeto precisa (sem valores reais)
- `.env` fica no `.gitignore` — nunca comite o arquivo real
- Valide as variáveis de ambiente na inicialização (validação de schema) para falhar rápido com mensagem clara

---

## Testes

### Localização
Espelhe `src/` dentro de `tests/`:
```
src/application/use-cases/tickets/create-ticket.ts
tests/application/use-cases/tickets/create-ticket.spec.ts
```

### Convenções
- Nomes de teste descrevem comportamento em linguagem simples
- Estrutura: `describe` por feature → `describe` por critério de aceitação → `it` por cenário
- Mocke todas as dependências externas (BD, auth, APIs) — nunca acesse serviços reais em testes unitários
- Um arquivo de teste por unidade

### Cobertura mínima
**90%** nas camadas `domain/` e `application/`. O QA garante isso na fase de TDD, antes de a implementação ser considerada concluída — ver `.ai/skills/tdd.md`.
