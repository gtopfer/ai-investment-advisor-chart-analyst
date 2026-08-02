# Especificação de Feature: Tickers extras e universo expansível

> **Prioridade:** P0 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário que analisa papéis fora da lista padrão
- **Eu quero** incluir tickers livres no universo candidato
- **Para que** a análise não fique presa às listas fixas do config

## 2. Requisitos & Restrições
- **R1**: Campo na sidebar (textarea) 'Tickers extras' — um por linha ou separados por vírgula.
- **R2**: Extras passam por normalize_ticker e entram em build_candidate_tickers (dedupe).
- **R3**: Tickers inválidos após normalização são ignorados com contagem/aviso leve.
- **R4**: Opcional no mesmo escopo: DEFAULT lists carregáveis de YAML/JSON em config/ se arquivo existir (senão listas atuais).
- **R5**: Testes: merge, dedupe, normalização crypto/BR.
- **Dependências:** Nenhuma
- **Desbloqueia / relacionada:** SPEC-018, SPEC-020, SPEC-030
- **Fora de escopo:** Screener completo da B3; upload de milhares de tickers sem paginação de progresso (isso é 018).

## 3. Expectativas de UI/UX (se aplicável)
- **Há interface de usuário?** Sim
- Detalhamento fino na fase UX (fluxos, estados, microcopy, design-premises).
- Prioridade de produto: **P0**

### Definition of Done — UX
- [ ] Superfícies e estados (loading/empty/error/success) definidos
- [ ] Microcopy-chave (CTAs, erros)
- [ ] Alinhado a design-premises
- [ ] Aceite humano na fase UX

## 4. Checklist Técnico / Notas
- portfolio/candidates.py + UI sidebar; config loader opcional.
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
