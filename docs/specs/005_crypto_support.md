# Especificação de Feature: Suporte completo a criptoativos

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário(a) interessado em cripto
- **Eu quero** que o app **funcione de ponta a ponta com criptomoedas**
- **Para que** eu possa analisar e simular carteiras com cripto com a mesma clareza que ações/FIIs/ETFs

## 2. Requisitos & Restrições

### Requisitos funcionais
1. Selecionar **Cripto** (sozinha ou com outras classes) e gerar carteira com criptoativos elegíveis de forma estável.
2. **Scoring justo**: para `asset_class == "Cripto"`, o `total_score` usa **apenas o componente técnico** (peso de dividendo = 0 para esse ativo), independente da estratégia da sidebar.
3. **Normalização de tickers**: aliases comuns (`BTC`, `ETH`, `SOL`, `BTCUSD`, …) → forma canônica Yahoo `SYMBOL-USD` quando for cripto conhecida/padrão.
4. **Lista padrão ampliada** (~10 principais em `*-USD` via yfinance).
5. **Labels de moeda honestos**: preços de cripto exibidos em **USD**; caption avisando que aporte/simulação pode misturar unidades quando há ativos multi-mercado.
6. Dividendos em cripto: score 0 e resumo **“não aplicável a cripto”** (sem ruído de “sem dados relevantes” genérico enganoso).
7. Import, rebalance e “Como deve ficar” funcionam com tickers normalizados.
8. Testes de normalização, scoring e classificação.

### Restrições
1. Fonte: yfinance apenas.
2. Sem wallet on-chain; sem FX automático USD→BRL no MVP.
3. Mistura BR (R$) + cripto (USD) permitida com **aviso**, não bloqueio.

## 3. Expectativas de UI/UX
- Help na classe Cripto / carteira: atalhos `BTC` ou `BTC-USD`.
- Preço cripto: `USD` na tabela.
- Caption de moeda mista quando houver CRYPTO no resultado.

## 4. Checklist Técnico / Notas
- Sem banco; sem novos pacotes.
- Módulos: `config`, normalização compartilhada, `allocator.score_assets`, `dividend_analysis` ou orquestração, `ui`, testes.
- ADR curto na technical-spec.

## 5. Definition of Ready (DoR)
- [x] Score: **só técnico para cripto**
- [x] Moeda: **labels USD + aviso**
- [x] Cobertura: **~10 principais + normalização**
- [x] Perguntas respondidas (2026-07-26)

## 6. Definition of Done (DoD)
- [x] Carteira só Cripto gera alocação com criptos quando dados existem
- [x] Aliases BTC/ETH normalizam e entram no fluxo
- [x] Cripto não penalizada por DY=0
- [x] Preço cripto não rotulado como R$
- [x] Testes passam; CHANGELOG/README atualizados

## 7. Decisões de produto fechadas (PM)
| Decisão | Valor |
|---------|--------|
| Score cripto | Técnico-only |
| Moeda | USD nos preços cripto + aviso de mistura |
| Tickers | ~10 + normalização |
| FX | Fora do MVP |
