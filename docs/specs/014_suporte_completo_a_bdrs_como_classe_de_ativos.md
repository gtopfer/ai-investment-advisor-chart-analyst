# Especificação de Feature: Suporte completo a BDRs como classe de ativos

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário focado em B3
- **Eu quero** marcar BDRs no multiselect e ver candidatos BDR na análise
- **Para que** eu possa alocar em recibos de ações estrangeiras listados na B3

**Contexto:** SPEC-008 removeu a opção morta “BDRs”. Esta feature **reintroduz com suporte real**.

## 2. Requisitos & Restrições
- **R1**: “BDRs” volta a constar em `ASSET_CLASS_OPTIONS` (multiselect).
- **R2**: Existe lista padrão de BDRs líquidos (tickers `.SA` via yfinance), configurável em `config` (ex. AAPL34.SA, MSFT34.SA, GOGL34.SA, AMZO34.SA, NVDC34.SA — lista final no Architect ≥ 5 tickers verificáveis).
- **R3**: `build_candidate_tickers` inclui a lista quando “BDRs” está selecionado (universo Nacional ou Ambos; Internacional sozinho **não** é obrigatório para BDRs B3 — se só Internacional, BDRs podem não entrar ou entrar se “BDRs” marcado independentemente: **regra de negócio:** BDRs são B3 → entram com **Nacional** ou **Ambos**; se universo só Internacional e BDRs marcado, ainda incluir BDRs **ou** mostrar caption — decisão: **incluir BDRs sempre que a classe estiver marcada**, independente do rádio de universo (evita armadilha).
- **R4**: `classify_ticker` classifica tickers da lista (e padrão heurístico de BDR se viável) como classe **BDRs**, mercado **BR**.
- **R5**: Preço/label em **R$** (como outros BR); scoring usa pesos de estratégia como ações (não regra cripto).
- **R6**: Testes: opções incluem BDRs; candidatos não vazios com só BDRs; classificação de ticker conhecido.
- **Restrição**: Sem conversão cambial USD→BRL além do preço já retornado pelo yfinance no ticker BDR.
- **Fora de escopo**: BDRs de todos os papéis da B3 dinamicamente; screener completo.

## 3. Expectativas de UI/UX
- **Há interface de usuário?** Sim (opção no multiselect; help opcional “BDRs listados na B3”)
- Empty se yfinance falhar em todos: mesmo fluxo de failed_tickers

### Definition of Done — UX
- [ ] Label/help
- [ ] design-premises
- [ ] Aceite UX

## 4. Checklist Técnico / Notas
- Banco: Não
- Pacotes: Não
- Reverter parcialmente SPEC-008 de forma consciente

## 5. Definition of Ready (DoR)
- [x] Claro
- [x] Lista mínima no Architect
- [x] BDRs entram se classe marcada (independente do universo)

## 6. Definition of Done (DoD)
- [ ] R1–R6 atendidos
- [ ] CHANGELOG; review APROVADO
