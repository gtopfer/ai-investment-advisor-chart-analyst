# Convenções

Padrões de código transversais, aplicáveis a qualquer linguagem usada neste workspace: nomenclatura, imports, comentários, commits.

> Arquitetura em camadas e stack: ver `architecture-guidelines.md`.
> Padrões específicos de backend: ver `backend-guidelines.md`.
> Padrões específicos de frontend: ver `frontend-guidelines.md`.

---

## Nomenclatura

Os nomes dos estilos abaixo (`kebab-case`, `camelCase` etc.) são termos técnicos universais — usados como estão em qualquer material técnico em português.

| Tipo | Padrão | Exemplo |
|------|---------|---------|
| Arquivos | `kebab-case` | `create-ticket.ts`, `board_card.py` |
| Funções / métodos | `camelCase` (ou padrão da linguagem, ex.: `snake_case` em Python/Rust) | `createTicket`, `create_ticket` |
| Classes / Tipos | `PascalCase` | `CreateTicketInput`, `BoardDto` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_ATTACHMENTS` |
| Variáveis / parâmetros | `camelCase` (ou padrão da linguagem) | `ticketId`, `ownerId` |

Siga a convenção própria da linguagem-alvo quando ela conflitar com a tabela acima (ex.: nomes exportados em Go são `PascalCase`, Python usa `snake_case` do início ao fim) — consistência com o ecossistema da linguagem vence a tabela.

---

## Imports

- Use aliases de caminho para imports internos quando a linguagem/ferramenta suportar (ex.: `@/` em TS/JS) em vez de caminhos relativos profundos (`../../../foo`).
- Evite arquivos barril (`index.ts` reexportando uma pasta inteira) — importe direto do módulo. Barris prejudicam tree-shaking, deixam o build mais lento e escondem dependências reais entre módulos.

---

## Conventional Commits

Todo commit segue o padrão **Conventional Commits** (os tipos abaixo são palavras-chave fixas do padrão — não são traduzidas, pois ferramentas de changelog/versionamento semântico dependem delas exatamente assim):

```
<tipo>(<escopo opcional>): <descrição curta no imperativo>
```

| Tipo | Quando usar |
|------|-------------|
| `feat` | Funcionalidade nova |
| `fix` | Correção de bug |
| `refactor` | Mudança de código sem alterar comportamento |
| `test` | Adição ou correção de testes |
| `docs` | Alteração de documentação |
| `style` | Formatação, espaçamento (sem mudança de lógica) |
| `chore` | Atualização de dependências/config/scripts |
| `ci` | Alterações em pipelines de CI/CD |

```bash
feat(tickets): adicionar criação de ticket via modal
fix(auth): corrigir redirecionamento após logout
refactor(use-cases): extrair validação compartilhada para DTO
test(tickets): adicionar testes de borda para exclusão lógica
chore: atualizar dependências para a versão estável mais recente
```

Regras:
- Modo imperativo, minúsculo: "adicionar", "corrigir", "extrair" — não "adicionado", "Corrigido"
- Máximo de 72 caracteres na primeira linha
- Breaking changes (mudanças que quebram compatibilidade): adicione `!` após o tipo (`feat!:`) e descreva no corpo do commit

---

## Comentários

- Comente somente quando a lógica não for óbvia pelo próprio código
- Não documente o óbvio (`// retorna o usuário` acima de `return user`)
- Prefira nomes autoexplicativos a comentários explicativos
