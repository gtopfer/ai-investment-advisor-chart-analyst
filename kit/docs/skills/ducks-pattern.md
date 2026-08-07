---
name: Ducks Pattern
type: architecture
category: organization
description: Modular code organization — group related code by feature, not by type
usedFor: [backend, frontend, organization]
appliesTo: [all]
requiredKnowledge: [modular-architecture, project-structure]
conflicts: [layer-by-type-folders]
mandatory: true
---

# Skill: Ducks Pattern (Guardrail)

## Quando usar

- Toda nova feature/domínio em projetos jojo-ai.
- Reorganização de código espalhado por tipo (`actions/`, `reducers/`, `types/`).

## Quando NÃO usar

- Utilities globais e componentes reutilizáveis → `src/shared/`.
- Shared cross-cutting (não é um “duck” de feature).

## O Que É

**Ducks Pattern** = Coloca tudo relacionado a um "conceito/feature" em uma pasta única, em vez de espalhado por `actions/`, `reducers/`, `types/`, etc.

```
❌ BAD (fragmentado):
src/
├── actions/
│   ├── users.js
│   └── posts.js
├── reducers/
│   ├── users.js
│   └── posts.js
├── types/
│   ├── USERS.js
│   └── POSTS.js

✅ GOOD (Ducks):
src/
├── ducks/
│   ├── users/
│   │   ├── actions.js
│   │   ├── reducer.js
│   │   ├── types.js
│   │   ├── selectors.js
│   │   └── index.js (exports)
│   └── posts/
│       ├── actions.js
│       ├── reducer.js
│       ├── types.js
│       ├── selectors.js
│       └── index.js (exports)
```

---

## Por Que É Obrigatório

1. **Coesão** — Código relacionado junto
2. **Escalabilidade** — Fácil adicionar features
3. **Testabilidade** — Mock/test um "duck" inteiro
4. **Manutenibilidade** — Achar o que precisa é óbvio
5. **Padronização** — Todos sabem onde procurar

---

## Estrutura Padrão de um Duck

```
src/ducks/[feature-name]/
├── types.ts          (Constants: ACTION_TYPES)
├── actions.ts        (Action creators)
├── reducer.ts        (State logic)
├── selectors.ts      (State queries)
├── utils.ts          (Helper functions)
├── constants.ts      (Feature-specific constants)
└── index.ts          (Public exports only)
```

### types.ts — Constants

```typescript
export const FETCH_USERS = 'users/FETCH_USERS'
export const FETCH_USERS_SUCCESS = 'users/FETCH_USERS_SUCCESS'
export const FETCH_USERS_ERROR = 'users/FETCH_USERS_ERROR'

export type User = {
  id: string
  name: string
  email: string
}

export type UsersState = {
  items: User[]
  loading: boolean
  error: string | null
}
```

### actions.ts — Action Creators

```typescript
import * as types from './types'

export const fetchUsers = () => ({
  type: types.FETCH_USERS,
})

export const fetchUsersSuccess = (users: types.User[]) => ({
  type: types.FETCH_USERS_SUCCESS,
  payload: users,
})

export const fetchUsersError = (error: string) => ({
  type: types.FETCH_USERS_ERROR,
  payload: error,
})
```

### reducer.ts — State Logic

```typescript
import * as types from './types'

const initialState: types.UsersState = {
  items: [],
  loading: false,
  error: null,
}

export default function reducer(
  state = initialState,
  action: any
): types.UsersState {
  switch (action.type) {
    case types.FETCH_USERS:
      return { ...state, loading: true }
    case types.FETCH_USERS_SUCCESS:
      return { ...state, items: action.payload, loading: false }
    case types.FETCH_USERS_ERROR:
      return { ...state, error: action.payload, loading: false }
    default:
      return state
  }
}
```

### selectors.ts — State Queries

```typescript
import { RootState } from '../../store'

export const selectUsers = (state: RootState) => state.users.items
export const selectUsersLoading = (state: RootState) => state.users.loading
export const selectUsersError = (state: RootState) => state.users.error

export const selectUserById = (id: string) => (state: RootState) =>
  state.users.items.find(u => u.id === id)
```

### index.ts — Public API (Exports Only)

```typescript
export * as types from './types'
export * as actions from './actions'
export * as selectors from './selectors'
export { default as reducer } from './reducer'
```

---

## Aplicável A

### Backend (Node.js)

```
src/features/
├── users/
│   ├── types.ts        (Interfaces, enums)
│   ├── controller.ts   (Request handlers)
│   ├── service.ts      (Business logic)
│   ├── repository.ts   (DB queries)
│   ├── routes.ts       (Express routes)
│   └── index.ts        (Exports)
├── posts/
│   └── (same structure)
```

### Frontend (React)

```
src/ducks/
├── ui/                 (Dialogs, modals, themes)
├── auth/               (Login, tokens, permissions)
├── users/              (User CRUD)
├── posts/              (Post CRUD)
```

### Qualquer Domínio

```
src/domains/
├── [domain-name]/
│   ├── types.ts
│   ├── [business-logic-1].ts
│   ├── [business-logic-2].ts
│   ├── utils.ts
│   └── index.ts
```

---

## Validação (Enforcement)

### Estrutura Obrigatória

Cada duck DEVE ter:
- [ ] `types.ts` — Tipos/constants
- [ ] Lógica principal (actions.ts, reducer.ts, controller.ts, service.ts)
- [ ] `selectors.ts` ou `queries.ts` — Forma pública de acessar
- [ ] `index.ts` — Public API (exports só o necessário)
- [ ] Sem exports diretos de arquivos internos (use index.ts)

### Verificação

```bash
# Script: validate-ducks.sh
for duck in src/ducks/*/; do
  if [ ! -f "$duck/types.ts" ]; then echo "❌ $duck missing types.ts"; fi
  if [ ! -f "$duck/index.ts" ]; then echo "❌ $duck missing index.ts"; fi
done
```

---

## Anti-Padrões

❌ **Não faça:**

```typescript
// ❌ Importar internals direto
import { someHelper } from 'src/ducks/users/utils.ts'

// ❌ Exports diretos sem index
export * from './actions.ts'
export * from './reducer.ts'

// ❌ Features em pastas aleatórias
src/utils/users/
src/helpers/posts/
src/lib/auth/

// ❌ Mixin de tipos de features
src/types/users.ts
src/types/posts.ts
```

✅ **Faça:**

```typescript
// ✅ Importar via index (public API)
import { actions, selectors } from 'src/ducks/users'

// ✅ Exports via index
// (index.ts controla o que é público)

// ✅ Tudo em ducks/[name]/ ou features/[name]/
src/ducks/users/
src/ducks/posts/

// ✅ Tipos com a feature
src/ducks/users/types.ts
src/ducks/posts/types.ts
```

---

## Checklist — Feature Nova

Ao criar nova feature:

- [ ] Criada pasta `src/ducks/[feature-name]/`
- [ ] `types.ts` com tipos + constants
- [ ] Lógica principal (actions/reducer ou service/repository)
- [ ] `selectors.ts` ou `queries.ts`
- [ ] `utils.ts` se houver helpers
- [ ] `index.ts` com public API
- [ ] Nenhum import direto de arquivo interno
- [ ] Tests em `__tests__/` na mesma pasta

---

## Exemplo Completo — Feature de Autenticação

```
src/ducks/auth/
├── types.ts
│   ├── User interface
│   ├── AuthState interface
│   ├── ACTION_TYPES constants
│
├── actions.ts
│   ├── loginRequest()
│   ├── loginSuccess(user)
│   ├── loginError(error)
│   ├── logout()
│
├── reducer.ts
│   ├── Initial state
│   ├── Handle all actions
│
├── selectors.ts
│   ├── selectUser()
│   ├── selectIsAuthenticated()
│   ├── selectError()
│
├── utils.ts
│   ├── parseJWT()
│   ├── validateToken()
│
├── __tests__/
│   ├── actions.test.ts
│   ├── reducer.test.ts
│   ├── selectors.test.ts
│
└── index.ts
    export { types, actions, selectors, reducer, utils }
```

Uso em outro componente:

```typescript
import { actions, selectors } from 'src/ducks/auth'

// ✅ Correto — via public API
const user = useSelector(selectors.selectUser)
dispatch(actions.loginRequest(email, password))
```

---

## Guardrail Obrigatório

**Este padrão é OBRIGATÓRIO em todo projeto que usa jojo-ai.**

Validação:
- [ ] Projeto segue Ducks Pattern
- [ ] Cada feature em pasta dedicada
- [ ] Public API clara (index.ts)
- [ ] Sem imports diretos de internals
- [ ] Tests colocation

---

**Quando usar:** Toda nova feature/domínio  
**Quando NÃO usar:** Utilities globais, componentes reusáveis (esses ficam em `src/shared/`)  
**Exceção:** Shared code vai em `src/shared/` (não em ducks/)

---

**Leia também:** `system-design.md` §2 (camadas e pastas **deste** projeto).  
Se §2 definir estrutura diferente de “ducks” nominal mas **coesa por feature**, siga o `system-design.md` e mantenha o espírito do padrão (feature-first, public API, sem pasta por tipo de arquivo).
