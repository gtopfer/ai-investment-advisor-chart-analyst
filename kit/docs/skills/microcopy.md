---
name: Microcopy
type: design
category: design
description: UI content design — CTAs, errors, empty states, labels
usedFor: [ui, ux, microcopy]
appliesTo: [frontend]
requiredKnowledge: [ux-writing, accessibility]
conflicts: []
---

# Skill: Microcopy (content design na UI)

## Quando usar

- Conforme a skill e a fase do runbook.

## Quando NÃO usar

- Fora do escopo do papel ativo ou sem artefato a validar.


> **Usado por**: UX Designer (fase `spec_approved`); PM (tom de produto); Developer (strings na implementação).  
> **Complementa**: `kit/docs/skills/ui-ux.md` e `system-design.md` § microcopy.

## Objetivo

Textos curtos da interface que **orientam a ação** e **reduzem erro**: botões, labels, empty states, erros, confirmações, tooltips.

## Princípios

1. **Clareza > cleverness** — diga o que acontece.  
2. **Verbo + objeto** nos CTAs (“Salvar filtro”, não “Ok”).  
3. **Uma ideia por mensagem**.  
4. **Erro = o que falhou + o que fazer**.  
5. **Consistência** de termos (o mesmo conceito, a mesma palavra).  
6. **Tom** alinhado a `system-design.md` (formal / direto / amigável).

## Checklist por tipo

### CTAs / botões

- [ ] Primário descreve o resultado (“Criar conta”), não o controle (“Enviar”)
- [ ] Destrutivo é explícito (“Excluir projeto”)
- [ ] Secundário não compete visualmente nem em wording com o primário
- [ ] Evitar “Clique aqui”

### Labels e placeholders

- [ ] Label permanente (não só placeholder)
- [ ] Placeholder como exemplo, não como única instrução
- [ ] Unidades e formato claros (“R$”, “DD/MM/AAAA”)

### Empty states

- [ ] Explica por que está vazio  
- [ ] Próximo passo (CTA) quando o usuário pode criar conteúdo  
- [ ] Sem culpar o usuário  

### Erros

| Evite | Prefira |
|-------|---------|
| “Erro 500” | “Não foi possível salvar. Tente de novo em instantes.” |
| “Inválido” | “Use um e-mail no formato nome@empresa.com” |
| Culpa genérica | Campo específico + correção |

- [ ] Inline no campo quando for validação  
- [ ] Banner/toast com retry quando for sistema/rede  
- [ ] Sem jargão de stack (exception, null, undefined)

### Confirmações destrutivas

- [ ] Nomeia o objeto (“Excluir **Projeto Alpha**?”)  
- [ ] Consequência se irreversível  
- [ ] Confirmar ≠ Cancelar ambíguo (“Excluir” / “Manter”)

### Loading / sucesso

- [ ] Loading: “Salvando…” (estado), não “Aguarde infinitamente”  
- [ ] Sucesso: confirmação curta se a UI não tornar o resultado óbvio  

## Glossário da feature

Antes de fechar a fase UX, liste 5–15 termos:

| Termo na UI | Significa | Não usar |
|-------------|-----------|----------|
| ex.: “Espaço” | workspace | “tenant”, “org” misturados |

## i18n

- Se o produto for só pt-BR: escreva em pt-BR nativo (não traduza mentalmente do inglês calqueado).  
- Se multi-idioma: chaves semânticas (`error.save_failed`), não frases concatenadas.

## Critérios de saída (com UI)

- [ ] CTAs principais definidos  
- [ ] Empty + error + sucesso cobertos  
- [ ] Glossário mínimo da feature  
- [ ] Tom alinhado às premissas  

## Anti-padrões

- Lorem ipsum em spec “para depois”  
- Três sinônimos para o mesmo botão em telas diferentes  
- Ironia ou humor em mensagens de erro  
- ELLIPSIS excessivo (“Salvando........”)  
