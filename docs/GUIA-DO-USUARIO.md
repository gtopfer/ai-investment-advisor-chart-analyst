# Guia do Usuário — DevKit-AI

**Este é o mapa contínuo do kit.** Leia na ordem na primeira vez; depois use como referência por fase.

Não é um app de demonstração: é o **roteiro humano** de como trabalhar com a IA e a CLI, do zero até a feature `done`.

---

## Como usar este guia

| Se você… | Vá para |
|----------|---------|
| Acabou de instalar o kit | [Capítulo 1](#capítulo-1--o-que-é-o-devkit-em-uma-frase) → [2](#capítulo-2--primeiro-dia-instalação) |
| Vai pedir a primeira feature | [Capítulo 4](#capítulo-4--a-primeira-feature-do-zero-ao-done) |
| Está no meio de uma fase e não sabe o que fazer | [Capítulo 5](#capítulo-5--cada-fase-explicada-para-você-humano) |
| A IA “pulou” etapas ou bagunçou o estado | [Capítulo 7](#capítulo-7--quando-algo-der-errado) |
| Quer só a colinha de comandos | [Capítulo 8](#capítulo-8--cola-rápida-comandos--frases-para-a-ia) |

---

## Capítulo 1 — O que é o DevKit, em uma frase

O DevKit-AI faz a IA **parar de improvisar código** e passar a trabalhar como um time pequeno com papéis claros:

```text
Você (humano)
    ↕ conversa + decisões
IA (um papel por vez: PM → UX → Architect → QA → Dev → …)
    ↕ só avança com
./devkit approve | reject | review
    ↕ progresso salvo em
.ai/state.md
```

Três ideias que não mudam nunca:

1. **Spec antes de código** — primeiro o *quê* e o *como*, depois a implementação.  
2. **Estado no disco** — se a sessão cair, o `state.md` sabe em que fase você parou.  
3. **Validação real** — `./devkit review` roda lint/testes de verdade, não “confiança” da IA.

Você **não** precisa ser programador de processos. Você precisa: (a) decidir o produto, (b) rodar um comando quando a fase pedir, (c) dizer “sim” ou “ainda não” com clareza.

---

## Capítulo 2 — Primeiro dia (instalação)

### 2.1 Colocar o kit no seu projeto

**Projeto novo ou pasta vazia:**

```bash
# a partir do repositório devkit-ai
./devkit init /caminho/do/seu-projeto
cd /caminho/do/seu-projeto
./devkit doctor
```

**Projeto que já tem código:**

```bash
/caminho/do/devkit-ai/devkit init .
./devkit doctor
```

O `init` **não apaga** o seu código de app. Ele instala a pasta `.ai/`, `docs/`, a CLI `devkit` e limpa só o *rastro de specs do meta-repo* (fica um slate limpo com `SPEC-000` done).

### 2.2 O que deve existir depois do init

- `./devkit` (executável)  
- `.ai/state.md` (painel de status)  
- `.ai/agents/` (papéis da IA)  
- `.ai/skills/` (como a IA executa TDD, UX, review…)  
- `docs/GUIA-DO-USUARIO.md` (este arquivo)

Se o `doctor` reclamar de arquivo ausente, re-rode o `init` ou restaure a pasta `.ai` a partir do kit.

### 2.3 Abrir a IA do jeito certo

1. Abra o chat **na raiz do projeto** (onde está o `./devkit`).  
2. A IA deve ler `.ai/global.instructions` e chamar o **Squad Lead**.  
3. Você não precisa “virar PM” sozinho: diga o que quer construir em português simples.

Frase de abertura sugerida:

> “Leia o DevKit (global.instructions + state). Rode `./devkit doctor` e `./devkit status`. Depois siga o Squad Lead.”

---

## Capítulo 3 — O mapa mental (sempre o mesmo filme)

Toda feature passa pela **mesma história**. Os nomes técnicos mudam; a lógica não.

```text
1. Entender o problema de negócio     →  PM          (draft)
2. Desenhar a experiência (ou N/A)    →  UX          (spec_approved)
3. Desenhar a construção técnica      →  Architect   (ux_approved)
4. Escrever testes que falham         →  QA          (tech_approved)
5. Implementar até os testes passarem →  Developer   (test_red)
6. Validar qualidade                  →  QA          (code_review)
7. Aceitar a entrega                  →  PM          (tested)
8. Fim                                →  done
```

Na CLI, cada seta “→” costuma ser um:

```bash
./devkit approve
```

Se a fase **falhou** (testes, DoD, UX rejeitada):

```bash
./devkit reject
```

### O que você vê no painel

```bash
./devkit status
```

Colunas importantes:

| Coluna | Significado para você |
|--------|------------------------|
| **Status** | Em que capítulo da história a feature está |
| **Fase Ativa** | Qual “personagem” da IA deve falar agora |
| **Código** | `SPEC-001`, `SPEC-002`… — o ID da feature |

Só a **primeira** spec que não está `done` recebe `approve`/`reject`.  
Para escolher outra: `./devkit activate SPEC-003`.

---

## Capítulo 4 — A primeira feature (do zero ao done)

Siga esta trilha **uma vez** sem pular. Depois fica automático.

### Passo 0 — Saúde do kit

```bash
./devkit doctor
./devkit status
```

### Passo 1 — Registrar a ideia

**Opção A — wizard:**

```bash
./devkit propose
```

**Opção B — direto (bom para a IA preencher):**

```bash
./devkit propose \
  --title "Filtro por status" \
  --persona "usuário logado" \
  --want "filtrar a lista por status" \
  --so-that "achar itens mais rápido" \
  --req "aceitar vários status" \
  --req "poder limpar o filtro"
```

Isso cria um arquivo em `.ai/specs/` e uma linha `draft` no `state.md`.

No chat:

> “Vamos detalhar a SPEC-00N juntos. Atue como PM.”

### Passo 2 — PM (você decide o *quê*)

A IA pergunta coisas de produto. Responda em linguagem de negócio:

- Quem usa?  
- O que é sucesso?  
- O que **não** entra nesta entrega?  
- Tem tela? (sim/não)

Quando a spec estiver redonda e o DoR marcado:

```bash
./devkit approve
```

Status vira `spec_approved` → fase **UX**.

### Passo 3 — UX (você decide a experiência)

- **Com tela:** a IA descreve fluxos, estados (loading/vazio/erro), textos de botão, alinhamento ao design system (`.ai/guidelines/design-premises.md`).  
  Na **primeira** feature com UI, preencha de verdade as premissas de marca (cores, lib de componentes, nav).  
- **Sem tela (API, job, CLI):** marque N/A na §3 da spec com um motivo honesto.

Aceitou o desenho?

```bash
./devkit approve
```

Status vira `ux_approved` → fase **Architect**.

### Passo 4 — Architect (você decide o *como* técnico de alto nível)

A IA propõe stack (se ainda for “a definir”), diagramas e contratos.  
Você não precisa gostar de todo jargão: pergunte “o que isso muda na prática?”.

Concordou?

```bash
./devkit approve
```

→ `tech_approved` / QA (TDD).

### Passo 5 — QA escreve testes que **falham**

Aqui **ainda não** há a feature pronta. É de propósito: os testes definem o comportamento.  
Você quase só observa; se a IA pedir regra de negócio ambígua, responda.

Quando os testes vermelhos existirem:

```bash
./devkit approve
```

→ `test_red` / Developer.

### Passo 6 — Developer implementa

A IA codifica e roda:

```bash
./devkit review
```

Só avance se o review disser **APROVADO**.

```bash
./devkit approve
```

→ `code_review` / QA validação.

### Passo 7 — QA valida de novo

Outro `./devkit review` (e a suíte).  
Passou → `approve`. Falhou → `reject` (volta para o Dev).

### Passo 8 — Você aceita a entrega (DoD)

A IA lista o Definition of Done.  
Cheque se o **comportamento** está ok (não “se o código é bonito”).

- Ok → docs/CHANGELOG + `./devkit approve` → **`done`**  
- Não ok → `./devkit reject` → Dev de novo  

### Passo 9 — Respire

```bash
./devkit status
./devkit log
```

A feature está no histórico. A próxima começa de novo no Passo 1.

---

## Capítulo 5 — Cada fase explicada (para você, humano)

### `draft` · Product Manager

| | |
|--|--|
| **Pergunta central** | O que estamos construindo e por quê? |
| **Seu papel** | Responder produto; recusar escopo infinito |
| **Arquivo que importa** | `.ai/specs/NNN_….md` |
| **Pronto quando** | Requisitos testáveis + DoR marcado + você disse sim |
| **Comando** | `./devkit approve` |

### `spec_approved` · UX / UI

| | |
|--|--|
| **Pergunta central** | Como a pessoa vive isso na interface (ou por que não há UI)? |
| **Seu papel** | Validar clareza, textos, estados vazios/erro; preencher design-premises se for a 1ª UI |
| **Arquivos** | §3 da spec, `.ai/features.feature`, `design-premises.md` |
| **Pronto quando** | DoD de UX ok **ou** N/A honesto |
| **Comando** | `./devkit approve` |

### `ux_approved` · Architect

| | |
|--|--|
| **Pergunta central** | Como o sistema se organiza para cumprir isso? |
| **Seu papel** | Aceitar trade-offs; bloquear overengineering se a feature for simples |
| **Arquivo** | `.ai/technical-spec.md` (+ guidelines de stack) |
| **Comando** | `./devkit approve` |

### `tech_approved` · QA (TDD)

| | |
|--|--|
| **Pergunta central** | Como sabemos, com testes, que está certo **antes** de existir o código? |
| **Seu papel** | Confirmar regras de borda se perguntarem |
| **Comando** | `./devkit approve` (testes vermelhos gravados) |

### `test_red` · Developer

| | |
|--|--|
| **Pergunta central** | Qual o menor código correto que deixa os testes verdes? |
| **Seu papel** | Não pedir “já que estamos aqui” features extras |
| **Comando** | `./devkit review` = APROVADO → `./devkit approve` |

### `code_review` · QA (validação)

| | |
|--|--|
| **Pergunta central** | Ainda passa tudo? Houve regressão? |
| **Comandos** | `review` + `approve` **ou** `reject` |

### `tested` · PM (DoD)

| | |
|--|--|
| **Pergunta central** | Posso dizer que a entrega está pronta para o usuário? |
| **Seu papel** | Aceite final de negócio |
| **Comandos** | `approve` → done **ou** `reject` |

---

## Capítulo 6 — O ritmo contínuo (semana a semana)

O DevKit brilha quando vira **hábito**, não evento único.

### Toda sessão nova (2 minutos)

```bash
./devkit doctor    # se algo parecer estranho
./devkit sync      # se você criou .md em specs/ na mão
./devkit status
./devkit log --limit 10
```

No chat:

> “Retome pelo Squad Lead a partir do state.md. Não reinvente a fase.”

### Uma feature por vez (recomendado no começo)

Várias specs `draft` ao mesmo tempo são ok, mas o `approve` só mexe na **primeira** da fila.  
Use `activate` para focar:

```bash
./devkit activate SPEC-004
```

### Emergência (produção quebrada)

```bash
./devkit hotfix --title "login 500" --reason "clientes offline"
```

Isso **pula** PM longo, UX e Architect e já entra em testes (QA).  
No final, o DoD **exige** que você documente o atalho no CHANGELOG. Hotfix não é atalho permanente de processo — é válvula de segurança.

### Projeto legado (já tinha código)

1. `init` no repo.  
2. Na primeira feature (ou num pedido só de baseline), peçà ao Architect mapear o que já existe em `architecture-guidelines.md` e `technical-spec.md`.  
3. Preencha `design-premises.md` se já houver UI real.  
4. Features novas seguem o Capítulo 4 normalmente.

---

## Capítulo 7 — Quando algo der errado

| Sintoma | O que fazer |
|---------|-------------|
| IA quer codar no meio do `draft` | “Não. Estamos no PM. Atualize a spec; sem código de produção.” |
| Status e fase “não combinam” (kit antigo) | `./devkit sync --migrate-lifecycle` |
| Spec no state mas arquivo sumiu | `doctor` mostra o erro; restaure o `.md` ou remova a linha do state |
| `review` reprovado | Deixe a IA corrigir (máx. ~3 tentativas na mesma causa); se travar, leia o log com ela |
| Você mudou a spec depois dos testes | Avisar o Squad Lead; pode precisar de `reject` até UX/PM |
| Duas features, approve na errada | `activate SPEC-…` antes do approve |
| `init` no próprio meta-repo devkit-ai | Bloqueado de propósito — init é para **outro** diretório |

### Frase mágica de recuperação

> “Ignore conversas antigas. Leia só `.ai/state.md`, a spec ativa e o agent da fase. Rode `status` e continue do gate atual.”

---

## Capítulo 8 — Cola rápida (comandos + frases)

### Comandos

```bash
./devkit doctor
./devkit status
./devkit sync
./devkit sync --migrate-lifecycle
./devkit propose
./devkit propose --title "…" --persona "…" --want "…" --so-that "…" --req "…"
./devkit activate SPEC-001
./devkit approve
./devkit reject
./devkit review
./devkit hotfix --title "…" --reason "…"
./devkit log
./devkit help
```

### Frases úteis no chat

| Momento | Frase |
|---------|--------|
| Início | “Squad Lead: sync + status e ative o agent da fase.” |
| PM | “Detalhe a SPEC-X; pergunte só o necessário; atualize o arquivo.” |
| UX | “Desenhe a §3 e o Gherkin; se não houver UI, N/A justificado.” |
| Architect | “Preencha technical-spec; use template se encaixar; liste trade-offs.” |
| Dev | “Implemente só o escopo da spec; rode review; não expanda escopo.” |
| Travado | “Pare no loop. Mostre as 3 tentativas e a decisão que precisa de mim.” |
| Fechar | “Valide o DoD item a item e prepare o CHANGELOG.” |

---

## Capítulo 9 — Onde mora cada verdade

| Pergunta | Arquivo |
|----------|---------|
| Em que fase estou? | `.ai/state.md` / `./devkit status` |
| O que o usuário ganha com a feature? | `.ai/specs/….md` |
| Como a UI se comporta? | §3 da spec + `.ai/features.feature` + `design-premises.md` |
| Como o sistema é construído? | `.ai/technical-spec.md` |
| Como a IA deve se comportar nesta fase? | `.ai/agents/*.agent.md` |
| Como fazer TDD / UX / review? | `.ai/skills/*` |
| O que mudou no produto? | `docs/CHANGELOG.md` |
| Este guia | `docs/GUIA-DO-USUARIO.md` |

Referência densa (árvore, diagrama Mermaid, lista completa da CLI): [`README.md`](../README.md) na raiz.

---

## Capítulo 10 — Mentalidade (para o kit “pegar”)

1. **Você é o dono da decisão; a IA é o time.**  
2. **Approve é um contrato**, não um enter por hábito.  
3. **Uma fase de cada vez** deixa o contexto da IA mais barato e mais correto.  
4. **Estado no disco > memória do chat.**  
5. **Hotfix existe para não mentir no processo** — use e documente, não normalize.  

Quando o fluxo estiver no automático, este guia vira só consulta. Até lá, volte ao [Capítulo 4](#capítulo-4--a-primeira-feature-do-zero-ao-done) sempre que abrir uma feature nova.

---

*DevKit-AI — guia contínuo do usuário. Melhore este arquivo quando o kit ganhar comando ou fase nova.*
