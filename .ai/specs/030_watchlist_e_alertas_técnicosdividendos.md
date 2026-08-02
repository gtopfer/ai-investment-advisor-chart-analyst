# Especificação de Feature: Watchlist e alertas técnicos/dividendos

> **Prioridade:** P3 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário que acompanha papéis pontuais
- **Eu quero** watchlist com alertas (RSI, DY, …)
- **Para que** eu revise ativos sem gerar carteira inteira

## 2. Requisitos & Restrições
- **R1**: Adicionar/remover tickers da watchlist (sessão + persist se 022).
- **R2**: Regras: RSI oversold/overbought, DY mínimo (reusar thresholds config).
- **R3**: Painel de alertas ativos após refresh/análise leve da watchlist.
- **R4**: Testes das regras de alerta com indicadores mock.
- **Dependências:** SPEC-017, SPEC-022
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** Push notification; email; alertas em tempo real websocket.

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
- novo módulo alerts/; UI seção.
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
