# Especificação de Feature: Classe BDRs — remover opção morta do multiselect

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário do dashboard de alocação
- **Eu quero** ver no seletor de classes **apenas** opções que realmente alimentam a análise
- **Para que** eu não marque “BDRs” achando que haverá candidatos e termine com lista vazia / análise sem sentido

**Decisão de produto (2026-07-26):** **Remover** a opção “BDRs” do multiselect. Não entregar suporte de universo BDR nesta feature. Tickers BDR digitados ou importados na carteira atual **continuam** podendo ser analisados se a fonte de dados os resolver (comportamento de ticker customizado, fora do universo padrão).

## 2. Requisitos & Restrições
- **R1**: A lista de classes de ativos oferecida na sidebar **não** inclui o item “BDRs”.
- **R2**: As classes oferecidas permanecem: **Ações**, **FIIs**, **ETFs**, **Cripto** (e nenhuma outra nova neste escopo).
- **R3**: `build_candidate_tickers` não precisa (e não deve) ter ramo “BDRs”; selecionar só classes válidas gera candidatos conforme regras já existentes (nacional/internacional/cripto).
- **R4**: Um ticker no formato BDR (ex.: `AAPL34.SA`) informado na carteira atual ou importado **não é rejeitado** só por ser BDR — segue o fluxo de ticker customizado / normalização já existente.
- **R5**: Testes automatizados comprovam R1–R4 (UI de opções via constante/fonte única **ou** asserção sobre a lista de classes exposta; candidatos e parse de ticker).
- **Restrição 1**: Não criar lista padrão de BDRs, nem classificação específica “BDRs” nesta entrega.
- **Restrição 2**: Sem mudança de scoring, alocação ou fontes de mercado além do necessário para R1–R5.
- **Fora de escopo**: Suporte completo a classe BDR (lista Yahoo, score dedicado, labels) — feature futura se demandada.

## 3. Expectativas de UI/UX (se aplicável)
- **Há interface de usuário?** Sim (sidebar / multiselect de classes).
- **Intenção de negócio**: o usuário não vê opção enganosa; o restante do fluxo de configuração permanece igual.
- **Microcopy**: sem texto novo obrigatório; se houver help da classe, não mencionar BDRs como opção de filtro.
- **Estados**: empty/error de “nenhum ativo” continuam valendo quando filtros legítimos não geram tickers (ex.: combinações impossíveis), mas **não** por causa de BDRs sozinho.

### Definition of Done — UX (fase `spec_approved`)
- [ ] Telas/superfícies: sidebar “Classes de ativos” sem “BDRs”
- [ ] Estados empty/error existentes não pioram
- [ ] Microcopy sem referência a BDRs como classe filtrável
- [ ] Alinhado a `.ai/guidelines/design-premises.md` (minimalista, sem opção morta)
- [ ] Aceite humano na fase UX

## 4. Checklist Técnico / Notas
- Precisa de mudança no banco de dados: Não
- Novos pacotes/dependências: Não
- Regras de segurança/permissão: N/A
- Ponto de mudança esperado: `ui/layout.py` (opções do multiselect); testes em `tests/test_app_filters.py` (e/ou teste de UI de opções se extrair constante compartilhada)
- Ideal: constante única `ASSET_CLASS_OPTIONS` (ou equivalente) consumida pela UI e pelos testes, para não “hardcodar BDRs” de novo

## 5. Definition of Ready (DoR — Pronto para Começar)
- [x] O problema de negócio e o resultado desejado estão claros
- [x] Dependências externas (APIs, credenciais, dados) estão disponíveis ou explicitamente adiadas
- [x] Perguntas em aberto foram respondidas por quem pediu (decisão: remover, não suportar)

## 6. Definition of Done (DoD — Pronto/Concluído)
- [ ] Todos os requisitos da seção 2 estão atendidos
- [ ] Os critérios de aceitação (cenários Gherkin) passam nos testes automatizados
- [ ] Documentação atualizada: entrada em `docs/CHANGELOG.md`; link em `docs/README.md` se aplicável
- [ ] Nenhuma regressão: Ações/FIIs/ETFs/Cripto e carteira importada/texto continuam funcionando
- [ ] `./devkit review` APROVADO na validação final
