# Especificação de Feature: Gráficos de preço no detalhe do ativo

> **Prioridade:** P3 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário do 'chart analyst'
- **Eu quero** ver série de preço no detalhe do ativo
- **Para que** a análise visual complemente indicadores numéricos

## 2. Requisitos & Restrições
- **R1**: No expander de detalhes: st.line_chart (ou equivalente) de Close.
- **R2**: Reusar histórico já baixado na run quando possível.
- **R3**: Fallback se insufficient_history.
- **R4**: Preferir zero deps novas (sem plotly obrigatório).
- **Dependências:** SPEC-024, SPEC-025
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** Candlestick completo, volume, overlays TA no gráfico.

## 3. Expectativas de UI/UX (se aplicável)
- **Há interface de usuário?** Sim
- Detalhamento fino na fase UX (fluxos, estados, microcopy, design-premises).
- Prioridade de produto: **P3**

### Definition of Done — UX
- [ ] Superfícies e estados (loading/empty/error/success) definidos
- [ ] Microcopy-chave (CTAs, erros)
- [ ] Alinhado a design-premises
- [ ] Aceite humano na fase UX

## 4. Checklist Técnico / Notas
- results UI; pass price series in last_run or re-fetch cached.
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
