# Spec: [FEATURE-XXX] [Título da Feature]

**Status:** `draft` (PM co-autoria)  
**Fases:** PM → UX → Architect → QA → Developer → QA Validação → PM DoD → Done  
**Data de Criação:** [AAAA-MM-DD]  
**Atualizado:** [AAAA-MM-DD]

---

## §1 Contexto & Valor

**Quem:** [Persona / tipo de usuário que vai usar]  
**Onde:** [Contexto: qual tela/fluxo do app]  
**Por quê:** [Problema que resolve ou valor que gera]  
**Quando:** [Se urgente, para quando; se recorrente, frequência]

**Exemplo bom:**
> Administradores de loja precisam gerar relatórios de vendas semanais sem abrir 3 ferramentas diferentes. Hoje levam 15 minutos; com isto leva 2.

---

## §2 Requisitos & Restrições

| # | Requisito | Tipo | Observação |
|----|-----------|------|-----------|
| R1 | [Descrição testável] | Funcional | [Limite/contexto se houver] |
| R2 | [Descrição testável] | Não-funcional | [Métrica/threshold] |
| R3 | [Edge case ou restrição] | Restrição | [Por quê] |

**Exemplo bom:**
| # | Requisito | Tipo | Observação |
|----|-----------|------|-----------|
| R1 | Usuário pode filtrar relatório por data | Funcional | Range: últimos 12 meses |
| R2 | Relatório gera em < 5s para 10k linhas | Não-funcional | Sem paginação visível |
| R3 | Exportação só em CSV (não PDF, não XLS) | Restrição | Restrição de produto/compliance |

---

## §3 Expectativas de UI/UX

**Tipo de interface:** [ ] Com UI visual (telas, fluxos, componentes) / [ ] Sem UI (API, CLI, job, infra) / [ ] N/A — Justificativa: [...]

### Se COM UI:

**Mapa de telas:**
1. Dashboard (lista de relatórios salvos)
2. Editor de relatório (filtros, preview)
3. Modal de confirmação de exportação

**Fluxo principal (happy path):**
```
Usuário clica "Novo Relatório"
  → Editor abre com filtros padrão
  → Usuário ajusta data/categoria
  → Preview atualiza em tempo real
  → Clica "Exportar"
  → Modal confirma
  → CSV baixa
```

**Estados por superfície:**
| Superfície | Loading | Empty | Error | Success |
|-----------|---------|-------|-------|---------|
| Lista | Skeleton 3 linhas | "Nenhum relatório" + CTA | "Erro ao carregar" + retry | Tabela com dados |
| Editor | Campos disabled | N/A | "Erro ao atualizar preview" | Preview atualizado |
| Exportação | Button desabilitado | N/A | "Falha na exportação" + retry | Download iniciado |

**Componentes de UI (design system):**
- Button primary (Exportar), secondary (Cancelar)
- Table with sorting
- DateRangePicker
- Modal Dialog
- Icons: download, refresh, alert

**Microcopy (textos, labels, mensagens):**
- CTA: "Gerar Relatório"
- Empty state: "Nenhum relatório gerado ainda. Clique aqui para começar."
- Error: "Não conseguimos atualizar o preview. Verifique sua internet e tente novamente."

**Responsividade:**
- Desktop: tabela completa
- Mobile: cards empilhados; exportação em menu drawer

**Acessibilidade:**
- Todos os botões alcançáveis por teclado (Tab)
- Labels associadas a inputs
- Contraste WCAG AA
- Aria-labels onde necessário

---

## §4 Checklist Técnico (Linguagem de Negócio)

- [ ] Comportamento observável sem ler código
- [ ] Dependências externas claras (ex: chamadas a API, banco de dados)
- [ ] Segurança considerada (autenticação, autorização)
- [ ] Performance esperada documentada
- [ ] Dados sensíveis (PII) não aparecem em logs/traces
- [ ] Compatibilidade com navegadores/SO esperada

---

## §5 Definition of Ready (DoR)

**Obrigatório antes de passar para UX/Arch:**

- [ ] Seções 1–4 preenchidas (sem placeholders `[...]` críticos)
- [ ] Cada requisito da §2 é testável (pass/fail claro)
- [ ] §3 preenchida ou marcada N/A com justificativa
- [ ] Nenhuma ambiguidade flagrante no chat
- [ ] Usuário confirmou no chat ("visto", "ok", aceita)

---

## §6 Definition of Done (DoD)

**Obrigatório para aceitar entrega final:**

- [ ] Feature implementada conforme §2 (todos R1–R3)
- [ ] Testes automatizados cobrem cenários principais (passa em CI)
- [ ] §3 UI/UX implementada com todos estados (se aplicável)
- [ ] Code review passou (`./jojo review` APROVADO)
- [ ] Sem TODOs/FIXMEs em código novo
- [ ] Relatório/changelog atualizado
- [ ] Sem regressões em features adjacentes (smoke test)
- [ ] Documentação (se aplicável) atualizada

---

## Fora de Escopo (Explícito)

- [ ] [O que NÃO será feito; deixe explícito para evitar surpresas]
- [ ] Exemplo: "Não faremos integração com Slack nesta feature; fica para v2"

---

## Notas

- [Qualquer detalhe adicional, decisão pendente, ou contexto histórico]
- [Exemplo: "PM pediu que fosse feito em 1 semana; scope é firme"]

---

**Próximo:** [Se está aqui com DoR ✓, próximo é UX Designer]
