# Guia de Frontend

Padrões de implementação para a camada de frontend: componentes, estado, roteamento, acessibilidade, estados de carregamento/erro, estilos.

> Stack e estrutura de camadas: ver `architecture-guidelines.md`.

---

## Responsabilidade dos Componentes

- Prefira componentes que só renderizam dados (listas, cards, tabelas) sem efeitos colaterais
- Extraia lógica não trivial (cálculos, derivações, handlers elaborados) para um módulo separado e testável isoladamente, ao lado do componente (ex.: `ticket-form.logic.ts` ao lado de `ticket-form.tsx`)
- Recorra a uma biblioteca de componentes de UI antes de construir um do zero; crie componentes próprios só quando há lógica de domínio real (ex.: um badge de status que mapeia status → cor) ou quando a customização não é viável com as variantes da biblioteca

---

## Estado no Cliente

Use a opção mais simples que resolve o problema, nesta ordem:

```
Estado na URL (query params) → estado local do componente → estado compartilhado/contexto → cache de estado do servidor (biblioteca de query)
```

| Tipo de estado | Solução preferida | Quando |
|------------|--------------------|----|
| Filtros, paginação, abas | Query params na URL | Compartilhável, linkável, sobrevive a refresh |
| UI local (modal aberto, toggle) | Estado local do componente | Efêmero, um único componente |
| Compartilhado entre componentes próximos | Lifted state + props | Mesma subárvore |
| Estado global de UI (tema, preferências) | Contexto | Lido por muitos, muda raramente |
| Dados do servidor com cache/refetch/mutação | Biblioteca de estado de servidor (TanStack Query, SWR etc.) | Quando server components/SSR sozinhos não bastam |

**Nunca duplique dados que pertencem ao servidor em estado global do cliente** — prefira re-buscar/revalidar a cachear manualmente.

---

## Roteamento

- Agrupe rotas logicamente sem poluir a URL quando o framework suportar (ex.: grupos de rota do Next.js)
- Mantenha layouts compartilhados no segmento de rota comum mais próximo
- Rotas de API pública/webhooks são o único uso aceitável de um route handler cru no lugar do padrão normal de tratamento de requisição da aplicação

---

## Estados de Carregamento e Erro

Toda rota ou view que realiza operações assíncronas precisa de um estado de carregamento explícito e um estado de erro explícito — prefira skeleton loaders a spinners genéricos para melhor performance percebida. Estados de erro devem oferecer uma ação de retry, não só uma mensagem.

---

## Acessibilidade (mínimo WCAG 2.1 AA)

- Não sobrescreva atributos ARIA que uma biblioteca de UI bem construída já define corretamente
- Componentes customizados devem incluir atributos ARIA corretos
- Toda imagem significativa tem um `alt` descritivo; imagens decorativas usam `alt=""`
- Todos os componentes interativos devem ser navegáveis via teclado
- Contraste mínimo: 4.5:1 para texto normal, 3:1 para texto grande

---

## Design Tokens e Estilos

- Use design tokens/variáveis CSS para cor, raio, espaçamento — nunca fixe valores que ignoram o tema
- Suporte uma variante/tema escuro para todo componente visual
- Estenda o sistema de tokens existente em vez de criar um paralelo

### Formulários
- Use uma biblioteca de validação orientada a schema como única fonte de verdade para validação e tipagem
- Mostre erros de campo diretamente abaixo do input
- Desabilite o submit enquanto o formulário está sendo enviado

---

## Variáveis de Ambiente (Frontend)

- Toda variável exposta ao bundle do navegador deve ser tratada como **pública**, nunca como segredo (frameworks como Next.js deixam isso explícito com um prefixo de nome como `NEXT_PUBLIC_`)
- Segredos, tokens e credenciais ficam só no servidor
- Valide as variáveis públicas em tempo de build para que configuração faltando falhe de forma visível, não silenciosamente como `undefined` em runtime
