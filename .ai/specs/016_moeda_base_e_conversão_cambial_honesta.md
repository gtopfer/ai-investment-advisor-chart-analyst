# Especificação de Feature: Moeda-base e conversão cambial honesta

> **Prioridade:** P0 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário com carteira multi-mercado (BR + US/cripto)
- **Eu quero** patrimônio, alvos e rebalance expressos em uma moeda-base coerente
- **Para que** eu não tome decisão misturando R$ e USD sem câmbio

## 2. Requisitos & Restrições
- **R1**: Seletor de moeda-base: BRL | USD (default BRL) **ou** modo mono-moeda que bloqueia classes incompatíveis — default de produto: **moeda-base BRL com conversão**.
- **R2**: Fonte de câmbio documentada (ex. yfinance par USDBRL=X ou endpoint explícito); falha de câmbio → aviso e não inventar taxa 1:1 silenciosa.
- **R3**: Totais (carteira atual, alvo, deltas do rebalance) exibidos na moeda-base com label claro (R$ ou USD).
- **R4**: Preços originais podem continuar na moeda do ativo; valores de alocação/rebalance na base.
- **R5**: Testes unitários: conversão, falha de FX, labels; sem rede obrigatória (mock da taxa).
- **Dependências:** Nenhuma
- **Desbloqueia / relacionada:** SPEC-020, SPEC-028, SPEC-029
- **Fora de escopo:** Hedging, múltiplas taxas históricas, PTAX oficial como única fonte regulatória.

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
- Novo módulo fx/ ou utils/fx.py; integrar em convert_positions e display; cache TTL da taxa.
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
