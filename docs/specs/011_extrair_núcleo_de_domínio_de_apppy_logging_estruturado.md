# Especificação de Feature: Extrair núcleo de domínio de app.py + logging estruturado

## 1. Contexto & Valor de Negócio
- **Como um(a)** desenvolvedor mantenedor
- **Eu quero** funções puras de classificação, candidatos e pipeline fora do orquestrador Streamlit, com logging em vez de print
- **Para que** o domínio seja testável sem runtime Streamlit e os erros de ticker sejam observáveis de forma profissional

## 2. Requisitos & Restrições
- **R1**: `classify_ticker`, `build_candidate_tickers` e helpers de parse de portfólio vivem fora de `app.py` (módulo(s) de domínio, ex. `portfolio/` ou `services/`).
- **R2**: `app.py` permanece orquestrador Streamlit (sidebar → pipeline → render); imports atualizados.
- **R3**: Erros ao processar ticker usam `logging` (não `print`); alinhado ao padrão de `analysis/ai_chart_engine.py`.
- **R4**: Testes existentes passam com imports atualizados; comportamento de classificação/candidatos/parse inalterado.
- **R5**: Funções de domínio usadas pelos testes não exigem `streamlit` em runtime de unit test (exceto testes de UI se houver).
- **Restrição**: Não migrar para Clean Architecture completa; manter pipeline em camadas documentado.

## 3. Expectativas de UI/UX
- Há interface de usuário? **Não** (refator interna; UX idêntica).

### Definition of Done — UX
- [x] N/A justificado

## 4. Checklist Técnico / Notas
- Banco: Não
- Pacotes: Não
- Atualizar technical-spec §5 se paths mudarem

## 5. Definition of Ready (DoR)
- [x] Claro
- [x] Preferível após SPEC-007 (parse unificado) e SPEC-006 (harness)
- [x] Sem perguntas em aberto

## 6. Definition of Done (DoD)
- [ ] R1–R5 atendidos
- [ ] review APROVADO; CHANGELOG + tech-spec se necessário
