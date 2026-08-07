---
name: UI/UX
type: design
category: design
description: Interface states, accessibility, consistency and microcopy
usedFor: [ui, ux, accessibility, microcopy]
appliesTo: [frontend]
requiredKnowledge: [design-systems, accessibility, responsive]
conflicts: []
---

# Skill: UI/UX (experiência, interface e consistência)

> **Usado por**: UX Designer (fase `spec_approved`); PM (rascunho de §3); Developer/QA (checagem de estados e a11y na implementação).  
> **Fonte de design (obrigatória):** `system-design.md` §3 (design system do projeto).  
> **Fonte de produto:** `agents.md` Seção 1.

## Quando usar

- Feature com qualquer superfície visual ou fluxo humano.  
- Review de usabilidade antes de `approve` da fase UX.  
- Diff de UI no Developer (estados, copy, a11y) em paralelo ao code-review.

## Quando NÃO usar

- API / job / CLI / infra sem superfície humana (marque N/A na §3 da spec **e** confirme `system-design.md` §3 = N/A).

## Fonte da verdade de design

1. Leia **`system-design.md` §3** antes de qualquer decisão visual.  
2. Tokens, lib de componentes, estados e microcopy do projeto **não se inventam no chat**.  
3. Se §3 estiver vazia: co-preencha `system-design.md` com o humano; só depois detalhe a feature na spec.  
4. Mudança de design system → atualizar `system-design.md` (+ aceite) antes do código.

## Princípios (ordem de prioridade)

1. **Clareza** — o usuário sabe onde está, o que pode fazer e o que aconteceu.  
2. **Consistência** — mesmos padrões do design system; zero “inventar de novo”.  
3. **Feedback** — toda ação assíncrona tem loading; toda falha tem erro + próximo passo.  
4. **Acessibilidade** — teclado, foco, contraste, labels (WCAG 2.1 AA mínimo).  
5. **Beleza subordinada à função** — estética serve à hierarquia e à marca, não ao contrário.

## Checklist de discovery (antes de desenhar)

- [ ] Persona e job-to-be-done claros na spec  
- [ ] Dispositivos-alvo definidos  
- [ ] Happy path em ≤ 7 passos (senão: simplificar ou fatiar feature)  
- [ ] Pelo menos 2 caminhos de falha ou borda identificados  
- [ ] Premissas de `system-design.md` §3 lidas (não contradizer)

## Checklist de interface (por tela/superfície)

Para **cada** tela/modal/drawer:

| Estado | Obrigatório? | Nota |
|--------|--------------|------|
| Default / populated | Sim | Conteúdo principal |
| Loading | Sim se async | Preferir skeleton a spinner genérico |
| Empty | Sim se lista/coleção | Mensagem + CTA se aplicável |
| Error | Sim se async/rede | Mensagem humana + retry |
| Submitting / disabled | Sim se form | Evitar double-submit |
| Partial / permission denied | Se auth | Explicar o que falta |

### Hierarquia e layout

- [ ] Um foco primário por view (um CTA principal)  
- [ ] Escaneável em F/Z: título → ação → detalhes  
- [ ] Densidade adequada à frequência de uso  
- [ ] Espaçamento e alinhamento via **tokens**, não magia de px soltos  

### Componentes

- [ ] Preferir biblioteca/design system declarado em `system-design.md` §3  
- [ ] Variantes semânticas (primary/destructive/ghost) usadas com intenção  
- [ ] Não recriar Button/Input/Modal existentes  

### Microcopy

- [ ] CTAs com verbo + objeto (“Salvar filtro”, não “Ok”)  
- [ ] Erros dizem o que falhou e o que fazer  
- [ ] Empty states ensinam o próximo passo  
- [ ] Tom alinhado à marca (formal / direto / etc.)

### Responsivo

- [ ] Breakpoints críticos cobertos (mobile e desktop no mínimo se ambos forem alvo)  
- [ ] Tabelas largas têm estratégia (scroll, cards, colunas prioritárias)  
- [ ] Touch targets ≥ ~44px em mobile  

### Acessibilidade

- [ ] Ordem de tab lógica  
- [ ] Foco visível  
- [ ] Labels em inputs (não só placeholder)  
- [ ] Contraste texto/ícones  
- [ ] Imagens: `alt` útil ou decorativo vazio  
- [ ] Não depender só de cor para status  

## Checklist de fluxo (UX)

- [ ] Entrada e saída do fluxo óbvias  
- [ ] Confirmação em ações destrutivas  
- [ ] Cancelar/voltar não perde dados sem aviso (quando houver rascunho)  
- [ ] Progresso em fluxos multi-etapa (se houver)  
- [ ] Deep link / URL state se a premissa exigir compartilhar filtros  

## Artefatos mínimos na spec (§3)

```markdown
### Telas
1. ...
### Fluxo principal
- ...
### Estados
| Tela | Loading | Empty | Error | ...
### Componentes (design system)
- ...
### Microcopy-chave
- ...
### A11y / responsivo
- ...
### Fora de escopo UI
- ...
```

## N/A (sem UI)

Só válido se a feature **não** altera nada que um humano veja em tela/app.

Registrar na spec:

```markdown
## 3. Expectativas de UI/UX
- N/A — [motivo: API interna / job batch / CLI only / ...]
```

## Critérios de saída (fase UX)

- [ ] §3 completa **ou** N/A justificado  
- [ ] Estados async cobertos  
- [ ] Gherkin com comportamento observável (se UI)  
- [ ] Consistente com `system-design.md` §3  
- [ ] Aceite humano no chat  
- [ ] Pronto para o Architect modelar contratos de dados da UI  

## Anti-padrões

| Evite | Faça |
|-------|------|
| “Deixa bonito depois” | Estados e fluxo primeiro |
| Tela única com 12 CTAs | Um primário + secundários claros |
| Erro só no console | Erro na UI com retry |
| Modal para fluxo de 10 campos | Página ou stepper |
| Nova cor hex solta | Token do sistema |
| Gherkin genérico | Cenários da feature real |

## Ligação com o kit

```
PM (draft) --approve--> UX (spec_approved) --approve--> Architect (ux_approved)
                              ui-ux.md
Developer/QA usam a mesma skill para não regredir estados/a11y.
```
