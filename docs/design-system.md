# Design System — AI Investment Advisor & Chart Analyst

**Versão:** 1.0  
**Atualizado:** 2026-08-07  
**Princípio:** minimalista · **monocromático** (escala azul-cinza) · dark-first  
**Implementação:** `ducks/ui/theme.py` · resumo em `system-design.md` §3

---

## 1. Princípios

| # | Princípio | Aplicação |
|---|-----------|-----------|
| 1 | **Minimalismo** | Poucos elementos; hierarquia por tipografia e espaço, não por cor de acento |
| 2 | **Monocromático** | Só tons da escala azul-cinza; **sem** verde/vermelho/amarelo de marca |
| 3 | **Clareza** | Um CTA primário por seção; estados empty/loading/error explícitos |
| 4 | **Consistência** | Tokens nomeados; proibido hex solto fora de `theme.py` |
| 5 | **Tom sóbrio** | Educacional; disclaimer visível; emojis mínimos |

**Fora do sistema:** light mode, brand color saturada, ícones ilustrativos pesados, animações decorativas.

---

## 2. Paleta (tokens de cor)

Escala do mais escuro → mais claro. Valores atuais (congelados nesta versão):

| Token | Hex | Uso |
| --- | --- | --- |
| `color.bg` | `#0f1419` | Fundo da app (`.stApp`) |
| `color.bg_elevated` | `#121820` | Empty state, painéis levemente elevados |
| `color.surface` | `#151b23` | Sidebar, cards de métrica |
| `color.border` | `#243041` | Bordas sólidas, divisor do disclaimer |
| `color.border_muted` | `#2a3a4d` | Borda dashed (empty) |
| `color.text` | `#e7ecf1` | Corpo / sidebar |
| `color.text_heading` | `#f3f6f9` | `h1`–`h3` |
| `color.text_muted` | `#8b9bb0` | Subtítulo, legal |
| `color.text_subtle` | `#9aabbf` | Empty state body |

### Regras de cor

- Status de recomendação (Compra / Aguardar / Evitar) usa **rótulo textual**, não só cor.
- Streamlit nativo (botões, inputs) herda o shell escuro; não sobrescrever com paletas coloridas.
- Gráficos: preferir a série padrão do Streamlit em tons neutros; evitar arco-íris.

---

## 3. Tipografia

| Papel | Padrão |
| --- | --- |
| Fonte | Streamlit default (sistema) |
| Heading weight | `600` |
| Heading tracking | `-0.02em` |
| Subtítulo | `0.95rem` · `color.text_muted` · classe `.main-subtitle` |
| Legal / disclaimer | `0.85rem` · `color.text_muted` · classe `.legal-note` |
| Corpo | herdado · `color.text` |

---

## 4. Espaçamento, raio e layout

| Token | Valor | Uso |
| --- | --- | --- |
| `radius.card` | `10px` | Métricas |
| `radius.empty` | `12px` | Empty state |
| `layout.max_width` | `1100px` | `.block-container` |
| page top padding | `1.5rem` | Conteúdo principal |
| section margin (legal) | `2rem` | Separação final |

Densidade: **média-alta** (dashboard de dados); preferir tabelas e métricas a cards decorativos.

---

## 5. Componentes e padrões de UI

### 5.1 Shell

- **Header:** título (`#`) + subtítulo (`.main-subtitle`)
- **Sidebar:** seções colapsáveis — Essencial · Carteira · Avançado
- **Main:** max-width 1100px, padding-top 1.5rem

### 5.2 Empty state (`.empty-state`)

- Borda dashed `border_muted`, fundo `bg_elevated`
- Título em `strong` (texto primário) + 3 passos orientando a primeira análise

### 5.3 Métricas

- `st.metric` estilizado como card: surface + border + radius 10px

### 5.4 Disclaimer (`.legal-note`)

- Sempre visível no rodapé dos resultados
- Tom educacional; sem linguagem de “dica de compra”

### 5.5 Resultados (ordem)

1. Métricas resumo  
2. Carteira alvo  
3. Alocação  
4. Rebalance  
5. “Como deve ficar”  
6. Detalhes técnicos (expander)  
7. Disclaimer  

### 5.6 Feedback

| Estado | Padrão |
| --- | --- |
| Loading | Spinner + progress do Streamlit |
| Empty | `.empty-state` com CTA implícito (configurar sidebar) |
| Import | “N importadas / M ignoradas” |
| Erro de ticker | lista de falhas; não derruba a análise |
| IA fallback | mensagem em PT-BR neutra |

### 5.7 Microcopy

- CTAs com verbo + objeto (“Gerar carteira”, “Importar”, “Salvar preferências”)
- Copy sóbria; PT-BR default + i18n EN em `ducks/ui/i18n.py`
- Emojis: só se o produto já expuser (ícone da app); evitar decoração em textos de domínio

---

## 6. Acessibilidade

- Contraste texto/fundo na escala dark (texto primário e muted sobre `bg`/`surface`)
- Status sempre com **texto** (não só cor)
- Labels em inputs (Streamlit)
- Foco nativo do browser/Streamlit

---

## 7. Mapeamento código

| Artefato | Path |
| --- | --- |
| Tokens + CSS | `ducks/ui/theme.py` (`TOKENS`, `dark_css()`) |
| Aplicação do tema | `ducks/ui/layout.py` → `apply_theme()` / `render_header()` |
| API pública UI | `ducks/ui/__init__.py` |
| Resumo arquitetural | `system-design.md` §3 |
| Strings UI | `ducks/ui/i18n.py` |

### Como alterar a paleta

1. Ajustar constantes em `ducks/ui/theme.py`  
2. Atualizar esta tabela e `system-design.md` §3  
3. Rodar testes de tema  

---

## 8. Checklist para features com UI

- [ ] Lê este arquivo + `system-design.md` §3  
- [ ] Não introduz hex fora de `theme.py`  
- [ ] Mantém monocromático (sem acento saturado)  
- [ ] Cobre empty / loading / error se houver async  
- [ ] Disclaimer permanece se a tela de resultados mudar  
- [ ] Microcopy alinhada ao tom educacional  

---

## 9. Histórico

| Versão | Data | Nota |
| --- | --- | --- |
| 1.0 | 2026-08-07 | Formalização da paleta já usada no tema escuro; tokens nomeados em código |
