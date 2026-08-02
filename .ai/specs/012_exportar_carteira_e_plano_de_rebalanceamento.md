# Especificação de Feature: Exportar carteira e plano de rebalanceamento

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário do dashboard
- **Eu quero** exportar a carteira alvo e o plano de rebalanceamento em CSV baixável
- **Para que** eu possa usar os números fora do app (planilha, corretora, arquivo)

## 2. Requisitos & Restrições
- **R1**: Após uma geração bem-sucedida (`last_run` com resultados), a UI oferece download de **dois** CSVs:
  1. **Carteira alvo** — tickers da carteira recomendada com valor e % de alocação (e campos úteis já exibidos na tabela).
  2. **Plano de rebalance** — ações (comprar/reduzir/zerar etc.), ticker, valores/deltas coerentes com a tabela de rebalance.
- **R2**: Formato CSV com cabeçalho legível em PT-BR ou nomes de coluna estáveis (documentados); encoding UTF-8.
- **R3**: Botões/links de export **não** aparecem (ou ficam desabilitados com mensagem) quando não há `last_run` / empty state.
- **R4**: Export reflete exatamente os dados da última execução exibida (incl. threshold de rebalance se a SPEC-015 já estiver aplicada no plano mostrado).
- **R5**: MVP **sem PDF** (decisão 2026-08-01).
- **Restrição**: Sem envio por e-mail; só download no browser.
- **Fora de escopo**: Excel (.xlsx), PDF, envio para API de corretora.

## 3. Expectativas de UI/UX (se aplicável)
- **Há interface de usuário?** Sim
- **Superfície**: bloco de resultados (próximo às tabelas de carteira e rebalance), tema escuro existente
- **Microcopy**: CTAs do tipo “Baixar carteira alvo (CSV)” e “Baixar plano de rebalance (CSV)”
- **Estados**: empty → sem botões; success → botões ativos; erro de geração → sem export daquela run

### Definition of Done — UX
- [ ] CTAs e posicionamento definidos
- [ ] Empty/disabled claro
- [ ] Microcopy PT-BR
- [ ] Alinhado a design-premises
- [ ] Aceite UX

## 4. Checklist Técnico / Notas
- Banco: Não
- Pacotes novos: Não (stdlib `csv` + `st.download_button`)
- Segurança: só dados já em memória da sessão

## 5. Definition of Ready (DoR)
- [x] Problema e resultado claros
- [x] Dependências N/A
- [x] Decisões fechadas: CSV only, dois arquivos, pós-`last_run`

## 6. Definition of Done (DoD)
- [ ] R1–R5 atendidos
- [ ] Testes cobrem geração do conteúdo CSV (unitário do builder)
- [ ] CHANGELOG + índice docs
- [ ] `./devkit review` APROVADO
