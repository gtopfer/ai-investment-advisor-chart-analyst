# Project Guidelines Template

**Crie isto no seu projeto em `.ai/guidelines/`** — customize para seu stack e contexto.

---

## architecture-guidelines.md

```markdown
# Arquitetura da Aplicação

## Stack Definido

| Camada | Stack | Versão | Justificativa |
|--------|-------|--------|---------------|
| Frontend | React | 18+ | Component-based, market standard |
| Backend | Node.js / Express | 18 LTS | JavaScript full-stack |
| Database | PostgreSQL | 14+ | ACID, relational |
| Job Queue | Redis | 7.0+ | Async, lightweight |
| Auth | JWT + Cookie | — | Stateless, secure |
| Testing | Jest + React Testing Library | Latest | Community standard |

## Padrões Arquiteturais

### Backend (Clean Architecture)

```
src/
├── domain/              # Pure business logic
│   ├── entities/        # Immutable objects
│   ├── use-cases/       # Use cases (orchestration)
│   └── errors/
├── application/         # DTOs, mappers
│   ├── dtos/
│   └── mappers/
├── adapters/            # Framework integration
│   ├── controllers/      # Express routes
│   ├── repositories/     # DB adapters
│   └── external-services/
└── infrastructure/      # Config, DB, logging
    ├── database/
    └── config/
```

### Frontend (Feature-based)

```
src/
├── features/
│   ├── reports/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types.ts
│   │   └── __tests__/
│   └── users/
├── shared/
│   ├── components/
│   ├── hooks/
│   ├── utils/
│   └── types/
└── config/
```

## Princípios de Decisão

1. **Simplicity First** — Não antecipe complexidade
2. **No Cross-feature Dependencies** — Features são silos
3. **Dependency Injection** — Inversão de controle explícita
4. **Test First** — TDD obrigatório em features novas
```

---

## design-premises.md

```markdown
# Design System & Product Premises

## Brand Identity

- **Cor primária:** #007AFF (azul, acessível)
- **Fonte:** Inter (sans-serif, web-safe)
- **Densidade:** Comfortable (não super compacta)

## Componentes Base

| Componente | Quando usar | Variações |
|-----------|-----------|-----------|
| Button | CTAs, ações | primary, secondary, danger |
| Input | Forms | text, email, password, number |
| Modal | Confirmações | alert, form, confirmation |
| Table | Dados estruturados | sortable, filterable, pagination |
| Card | Agrupamento de info | elevated, outlined, flat |

## Padrões de UX

1. **Loading states:** Skeleton + 300ms min (evita flickering)
2. **Empty states:** Ícone + texto descritivo + CTA
3. **Error handling:** Toast notification + retry button
4. **Forms:** Validação inline; erro em vermelho; helper text em cinza
5. **Mobile-first:** Desktop é enhancement, não redução

## Acessibilidade (WCAG 2.1 AA)

- Contraste: 4.5:1 (texto), 3:1 (gráficos)
- Teclado: Tab order lógica
- Cores: Não use cor sozinha para transmitir info
- Labels: Todos inputs têm label associada
```

---

## conventions.md

```markdown
# Code Conventions

## Commits

```
<type>(<scope>): <subject>

<body>
```

- Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`
- Scope: feature/componente (ex: `refactor(export): use streaming`)
- Subject: imperativo, sem ponto

## Naming

### Backend (TypeScript/Node)

- **Classes:** PascalCase (`UserRepository`, `ExportWorker`)
- **Functions:** camelCase (`fetchUser`, `generateCsv`)
- **Constants:** UPPER_SNAKE_CASE (`MAX_RETRIES = 3`)
- **Files:** kebab-case (`user-repository.ts`)

### Frontend (React)

- **Components:** PascalCase (`UserProfile`, `ReportTable`)
- **Hooks:** camelCase, prefix `use` (`useReports`, `useFetch`)
- **Files:** kebab-case (`user-profile.tsx`)
- **Constants:** UPPER_SNAKE_CASE (`DEFAULT_PAGE_SIZE`)

## Code Style

- **Formatter:** Prettier (no semicolons, 2-space indent)
- **Linter:** ESLint + `@typescript-eslint`
- **Type checking:** TypeScript strict mode (`noImplicitAny: true`)
- **Tests:** Jest; file naming `*.test.ts` ou `*.spec.ts`

## Comments

- No por padrão (código auto-documentado)
- Sim se: "por quê" não é óbvio (workaround, decisão não-trivial)
- Nunca: "o que o código faz" (refatore em vez disso)

```

---

## frontend-guidelines.md

```markdown
# Frontend Guidelines (React)

## Component Structure

```typescript
// MyComponent.tsx
import { FC, ReactNode } from 'react'
import styles from './MyComponent.module.css'

interface MyComponentProps {
  title: string
  children: ReactNode
  onClose?: () => void
}

export const MyComponent: FC<MyComponentProps> = ({
  title,
  children,
  onClose,
}) => {
  return (
    <div className={styles.container}>
      <h2>{title}</h2>
      {children}
    </div>
  )
}
```

## State Management

- **Local state:** `useState` (um componente)
- **Shared state:** Context API (< 5 componentes)
- **Global state:** Redux (> 5 componentes, complexo)

## API Integration

```typescript
// Use React Query + custom hooks
import { useQuery } from '@tanstack/react-query'

export function useReports(userId: string) {
  return useQuery({
    queryKey: ['reports', userId],
    queryFn: () => api.get(`/reports?user_id=${userId}`),
  })
}
```

## Performance

- **Lazy load:** componentes heavy (`React.lazy`)
- **Code split:** por rota
- **Images:** otimizadas; use webp com fallback
- **Bundle:** monitorar com `bundlesize` npm script

## Acessibilidade

- `aria-label` em botões sem texto
- `aria-hidden="true"` em ícones decorativos
- Foco visível em `.focus-visible`
- Formulários: `<label htmlFor="id">` + `<input id="id">`

```

---

## backend-guidelines.md

```markdown
# Backend Guidelines (Node.js / Express)

## Project Structure

```
src/
├── domain/
│   ├── user/
│   │   ├── User.ts (entity)
│   │   ├── UserRepository.ts (interface)
│   │   └── CreateUserUseCase.ts
│   └── report/
├── application/
│   ├── dto/
│   └── mappers/
├── adapters/
│   ├── controllers/
│   ├── repositories/ (PostgreSQL impl)
│   └── external-services/
├── infrastructure/
│   ├── database/ (connection, migrations)
│   └── config/
└── app.ts (Express setup)
```

## Request/Response Pattern

```typescript
// Controller (adapter)
app.get('/users/:id', async (req, res) => {
  try {
    const user = await getUserUseCase.execute(req.params.id)
    res.json(UserMapper.toPersistence(user))
  } catch (error) {
    if (error instanceof NotFoundError) {
      res.status(404).json({ error: 'User not found' })
    } else {
      res.status(500).json({ error: 'Internal error' })
    }
  }
})
```

## Error Handling

- Custom error classes (`NotFoundError`, `ValidationError`, `UnauthorizedError`)
- Stack traces em logs; nunca envie ao cliente
- User-friendly messages em respostas

## Testing (Jest)

- Unit: `domain/`, `application/` (mocks de tudo)
- Integration: `adapters/` (DB real, HTTP mock)
- E2E: rotas completas contra DB teste

## Performance & Security

- Rate limiting: 100 req/min por IP padrão
- CORS: whitelisted domains
- SQL Injection: always use parameterized queries (Prisma, TypeORM)
- Secrets: use `dotenv`, nunca commit `.env`

## Ducks Pattern (Obrigatório)

Organize código por feature, não por tipo:

```
src/ducks/                    ✅ CORRETO
├── users/
│   ├── types.ts
│   ├── actions.ts
│   ├── reducer.ts
│   ├── selectors.ts
│   └── index.ts
└── posts/
    ├── types.ts
    ├── actions.ts
    ├── reducer.ts
    ├── selectors.ts
    └── index.ts

src/
├── actions/               ❌ ERRADO
├── reducers/
├── types/
```

**Regras:**
- Cada feature em pasta própria
- `index.ts` controla public API
- Sem imports diretos de internals
- Tudo relacionado à feature junto
- Exceção: Shared code em `src/shared/`

Veja `docs/skills/ducks-pattern.md` para detalhes.

```

---

## Exemplo: Checklist para Nova Feature

Antes de começar a code, garanta:

- [ ] Spec lida (§1–§4)
- [ ] `.ai/guidelines/*` lidos (stack, padrões, paths)
- [ ] Contratos definidos em tech-spec
- [ ] Testes RED prontos (QA)
- [ ] UI mockups aprovados (se houver)

---

**Use isto como template:** Copie para `seu-app/.ai/guidelines/` e customize!
