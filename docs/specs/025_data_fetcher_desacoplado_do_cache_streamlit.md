# Especificação de Feature: Data fetcher desacoplado do cache Streamlit

> **Prioridade:** P2 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** desenvolvedor
- **Eu quero** fetch de mercado testável sem st.cache_data
- **Para que** unit tests e modo offline não dependam do runtime Streamlit

## 2. Requisitos & Restrições
- **R1**: API pura get_price_history_raw etc. + wrapper com cache para app.
- **R2**: TTL ~900s preservado no caminho Streamlit.
- **R3**: test_market_data não precisa de st.cache real.
- **R4**: Contratos de DataFrame/dict para analysis/ inalterados.
- **Dependências:** Nenhuma
- **Desbloqueia / relacionada:** SPEC-018, SPEC-033, SPEC-026
- **Fora de escopo:** Redis/shared cache multi-instância.

## 3. Expectativas de UI/UX (se aplicável)
- **Há interface de usuário?** Não — Sem UI de produto
- Prioridade: **P2**

### Definition of Done — UX
- [x] N/A justificado

## 4. Checklist Técnico / Notas
- data_fetcher/ split core vs streamlit_cache.
- Banco de dados: Não (salvo se Architect excepcionar)
- Novos pacotes: só se justificado na tech-spec
- Segurança: não persistir/logar API keys nem senha de IA

## 5. Definition of Ready (DoR)
- [x] Problema e valor claros (auditoria de melhorias)
- [x] Prioridade e dependências registradas
- [ ] Decisões finas de produto (se restarem) fechadas no chat PM antes do approve
- [x] Critérios de aceite testáveis nos requisitos

## 6. Definition of Done (DoD)
- [ ] Todos os requisitos da §2 atendidos
- [ ] Testes automatizados cobrem caminhos críticos
- [ ] `docs/CHANGELOG.md` + link em `docs/README.md` / backlog
- [ ] `./devkit review` APROVADO
- [ ] Tech-spec §9 se houver decisão arquitetural
