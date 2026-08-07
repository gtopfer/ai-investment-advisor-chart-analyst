# ADR: [Título da Decisão]

**Data:** [AAAA-MM-DD]  
**Status:** Proposto | Aceito | Depreciado  
**Contexto da Feature:** [Link ou ref para spec, ex: FEATURE-001]  
**Autor(a):** [Architect ou decision maker]

---

## 1. Questão Arquitetural

[O que precisa ser decidido? Por quê?]

**Exemplo:**
> Como armazenar cache de relatórios: em-memória (Redis) vs. banco de dados vs. filesystem local?

---

## 2. Opções Consideradas

### Opção A: [Nome]
**Prós:**
- ...

**Contras:**
- ...

**Trade-offs:**
- ...

### Opção B: [Nome]
**Prós:**
- ...

**Contras:**
- ...

**Trade-offs:**
- ...

### Opção C: [Nome]
**Prós:**
- ...

**Contras:**
- ...

**Trade-offs:**
- ...

---

## 3. Decisão

**Escolhido:** [Opção X] — porque [1–2 linhas de justificativa]

**Impacto:**
- [ ] Muda database schema
- [ ] Muda endpoints/contratos
- [ ] Muda padrão de código
- [ ] Muda infra (recursos, CI/CD)
- [ ] Afeta performance / escalabilidade
- [ ] Afeta segurança

---

## 4. Consequências

**Positivas:**
- ...

**Negativas:**
- ...

**Mitigações (se houver risco residual):**
- ...

---

## 5. Alternativas Rejeitadas & Por Quê

| Opção | Motivo |
|-------|--------|
| [Opção X] | [Causa raiz da rejeição] |

---

## 6. Próximas Decisões

[Se esta decisão abre questões arquiteturais futuras, cite aqui]

**Exemplo:**
> Próxima: como fazer versionamento de cache? Timestamp simples? Hash de conteúdo?

---

## 7. Referências

- [Link para doc de contexto]
- [Link para spike/prova de conceito se houver]
- [Links para ADRs relacionadas]

---

## 8. Changelog

| Data | Status | Mudança |
|------|--------|---------|
| [AAAA-MM-DD] | Proposto | Criado ADR |
| [AAAA-MM-DD] | Aceito | [Quem] confirmou em [contexto] |

---

**Append-only:** Nunca apague ADRs antigas. Se mudar de ideia, crie um novo ADR explicando por quê.
