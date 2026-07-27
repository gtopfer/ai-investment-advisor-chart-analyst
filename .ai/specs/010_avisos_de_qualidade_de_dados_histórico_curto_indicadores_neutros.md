# Especificação de Feature: Avisos de qualidade de dados (histórico curto)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário do dashboard
- **Eu quero** ser avisado quando um ativo não tem histórico suficiente para indicadores técnicos confiáveis
- **Para que** eu não interprete scores neutros silenciosos como análise completa

## 2. Requisitos & Restrições
- **R1**: A análise técnica identifica ativos com histórico **insuficiente** para o cálculo padrão (regra alinhada a `analyze_chart_patterns`: tipicamente **&lt; 50** candles / pontos de preço usáveis).
- **R2**: Após gerar a carteira, a UI exibe um **aviso observável** listando tickers com histórico insuficiente (ou equivalente claro no detalhe).
- **R3**: A fórmula de score **não** muda neste escopo (apenas transparência).
- **R4**: Se nenhum ticker for afetado, nenhum aviso extra de “histórico curto” é mostrado.
- **R5**: Testes unitários cobrem detecção; teste ou contrato cobre exposição do sinal para a UI.
- **Restrição**: Sem novos provedores de dados; sem conversão cambial.

## 3. Expectativas de UI/UX
- Há interface de usuário? **Sim**
- Superfície: área de resultados pós-geração (warning Streamlit ou lista no bloco de detalhes).
- Microcopy (PT-BR): algo como “Histórico insuficiente para indicadores completos: TICKER1, TICKER2”.
- Estados: success da análise + warning opcional; não bloqueia a geração.

### Definition of Done — UX
- [ ] Aviso visível, legível, no tema escuro existente
- [ ] Não polui empty state
- [ ] Microcopy definida
- [ ] Alinhado a design-premises
- [ ] Aceite UX

## 4. Checklist Técnico / Notas
- Banco: Não
- Pacotes novos: Não
- Sinal possível: flag em `TechnicalIndicators` ou lista em `session_state.last_run`

## 5. Definition of Ready (DoR)
- [x] Claro
- [x] Dependências N/A
- [x] Decisão: aviso informativo, sem mudar score

## 6. Definition of Done (DoD)
- [ ] R1–R5 atendidos
- [ ] Gherkin/testes passam
- [ ] CHANGELOG atualizado
- [ ] review APROVADO
