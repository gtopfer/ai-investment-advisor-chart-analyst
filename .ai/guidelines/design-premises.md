# Premissas de Design & Produto

Este arquivo contém as diretrizes permanentes de UI/UX, regras de design system e premissas gerais do produto. 

> **Atenção IA**: Toda decisão de design de interface, fluxo de usuário, escolhas de bibliotecas visuais ou arquitetura técnica deve obrigatoriamente respeitar as premissas descritas neste documento.

---

## 1. Premissas de UI (Interface do Usuário) & Design System

*Escreva aqui a stack visual, biblioteca de componentes, paleta de cores ou regras estéticas da aplicação.*

- **Biblioteca de UI/UX**: [ex: Tailwind CSS + shadcn/ui | Vanilla CSS + HTML puro]
- **Temas**: [ex: Suporte obrigatório a Dark/Light mode | Dark mode padrão]
- **Tipografia**: [ex: Fonte Inter para texto, Outfit para títulos]
- **Cores Preferidas**: 
  - Primária: [ex: HSL(220, 100%, 50%) - Azul premium]
  - Neutra: [ex: HSL(224, 71%, 4%) - Dark slate para fundo]

---

## 2. Premissas de UX (Experiência do Usuário)

*Escreva aqui como as interações devem se comportar na aplicação.*

- **Navegação**: [ex: Menu lateral fixo (Sidebar) no desktop, gaveta (Drawer) em mobile]
- **Formulários**: [ex: Sempre usar modais suspensos (Dialogs) para inserções rápidas, ou páginas dedicadas para fluxos longos]
- **Estados de Interação**:
  - Toda chamada assíncrona deve exibir skeleton loader e desabilitar botões de submit.
  - Mensagens de erro devem fornecer um botão de tentar novamente (retry).

---

## 3. Premissas Técnicas Globais & de Engenharia

*Escreva aqui as diretrizes gerais de engenharia do projeto.*

- **Padrão de Comunicação**: [ex: Preferir Server Actions em Next.js para mutações, REST APIs para queries externas]
- **Persistência**: [ex: Usar SQLite local para desenvolvimento e PostgreSQL para produção]
- **Acessibilidade**: Mínimo WCAG 2.1 AA (atributos ARIA apropriados, navegação por teclado e contraste adequado).
