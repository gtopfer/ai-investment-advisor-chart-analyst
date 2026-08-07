# Especificação de Feature: Importar carteira atual

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário(a) que já tem posições em planilha ou exportação simples
- **Eu quero** **importar** minha carteira atual a partir de arquivo
- **Para que** o plano de rebalanceamento use minhas posições reais com menos esforço e menos erro de digitação

## 2. Requisitos & Restrições

### Baseline atual
- Carteira atual = text area (`TICKER, VALOR` ou quantidade; separadores `,` `;` `:`).
- Parser: `parse_current_portfolio`; modo UI: “Valor atual (R$)” vs “Quantidade de cotas/unidades”.

### Requisitos funcionais
1. **Upload de arquivo** na seção Carteira atual para carregar posições usadas no rebalanceamento.
2. **Formatos MVP**:
   - **CSV** (cabeçalho opcional; colunas reconhecidas de forma simples — ex. `ticker` + `valor` ou `ticker` + `quantidade` / segunda coluna numérica).
   - **TXT** no mesmo formato linha a linha já aceito pelo parser atual.
3. **Interpretação numérica** segue o **modo da UI** já existente (Valor R$ vs Quantidade): a coluna numérica do arquivo é lida nesse modo; o import não inventa um terceiro modo.
4. **Substituir tudo**: um import bem-sucedido **substitui** o conteúdo atual da carteira na sessão (não mescla com o texto anterior).
5. **Pós-import editável**: o resultado preenche a text area (ou equivalente editável) para o usuário ajustar antes de “Gerar carteira”.
6. **Feedback**: informar quantas posições foram importadas e quantas linhas foram ignoradas (motivo resumido: formato inválido, ticker inválido, valor ≤ 0, etc.).
7. **Import parcial**: linhas ruins não abortam o restante; se zero linhas válidas, aviso claro e carteira não é sobrescrita com vazio por engano (manter anterior ou deixar explícito o estado — preferência: **não substituir** se zero válidas).
8. **Entrada manual preservada**: colar/digitar continua funcionando sem arquivo.
9. **Modelo CSV baixável**: controle “baixar exemplo” com formato documentado (2–3 linhas de amostra).
10. **Somente arquivo local** via Streamlit; **sem** integração com API de corretora (B3/CEI/etc.) neste ciclo.
11. **Sem persistência** da carteira entre sessões do navegador (session only).

### Restrições
1. Não alterar score, alocação ou coleta de mercado — só a origem do mapa de posições atuais.
2. Processar em memória; não salvar uploads no repositório.
3. Limite razoável de tamanho/linhas (Architect define número; ex. evitar arquivos enormes na sessão Streamlit).
4. Excel (`.xlsx`) e APIs de corretora: **fora do MVP**.

## 3. Expectativas de UI/UX
- Na seção **Carteira atual** (sidebar colapsável da SPEC-002, ou equivalente atual):
  - `file_uploader` (CSV/TXT)
  - Botão/link **Baixar modelo CSV**
  - Text area continua visível e é **substituída** após import com linhas válidas
- Mensagens de sucesso/aviso em PT-BR, discretas (alinhadas ao visual minimalista).
- Help curto: “Colunas: ticker e valor (ou quantidade, conforme o modo acima)”.

## 4. Checklist Técnico / Notas
- Precisa de mudança no banco de dados: **Não**
- Novos pacotes/dependências: **Não esperado** (CSV/TXT com stdlib/`pandas` já presente)
- Segurança: validar tickers com as mesmas regras do parser atual; não executar conteúdo
- Testes: unitários de parse de CSV/TXT, substituição, zero válidas, modo valor vs quantidade
- Documentar formato no README

## 5. Definition of Ready (DoR — Pronto para Começar)
- [x] Problema e valor claros
- [x] Formatos MVP: **CSV + TXT**
- [x] Política: **substituir tudo** (exceto se zero linhas válidas → não sobrescrever)
- [x] Modo numérico: **respeita seletor da UI**
- [x] Extra MVP: **modelo CSV baixável**; sem API corretora
- [x] Perguntas em aberto respondidas (2026-07-26)

## 6. Definition of Done (DoD — Pronto/Concluído)
- [x] Requisitos da seção 2 atendidos
- [x] Import CSV e TXT válidos preenchem a carteira e alimentam o rebalanceamento
- [x] Modelo CSV baixável disponível na UI
- [x] Entrada manual intacta
- [x] Zero linhas válidas → aviso e carteira anterior preservada
- [x] Testes automatizados do import/parser
- [x] `docs/CHANGELOG.md` + README (formato + exemplo)
- [x] Sem regressão no rebalanceamento existente

## 7. Critérios de aceitação (rascunho Gherkin)

```gherkin
# language: pt
Funcionalidade: Importar carteira atual

  Cenário: Importar CSV válido substitui a carteira
    Dado que a text area da carteira atual tem posições antigas
    E o modo está em "Valor atual (R$)"
    Quando o usuário importa um CSV com tickers e valores válidos
    Então a carteira atual passa a refletir apenas as posições do arquivo
    E o usuário vê quantas posições foram importadas

  Cenário: Importar TXT no formato linha a linha
    Dado um arquivo .txt com linhas "TICKER, VALOR"
    Quando o usuário importa o arquivo
    Então as posições válidas preenchem a carteira atual

  Cenário: Linhas inválidas não quebram o import
    Dado um CSV com algumas linhas válidas e outras inválidas
    Quando o usuário importa o arquivo
    Então as linhas válidas são aplicadas
    E um aviso resume quantas linhas foram ignoradas

  Cenário: Nenhuma linha válida preserva a carteira
    Dado que a carteira atual já tem posições
    Quando o usuário importa um arquivo sem nenhuma linha válida
    Então a carteira anterior permanece
    E uma mensagem de erro/aviso é exibida

  Cenário: Modelo CSV disponível
    Quando o usuário solicita o modelo de exemplo
    Então recebe um CSV com o formato documentado
```

## 8. Decisões de produto fechadas (PM)
| Decisão | Valor |
|---------|--------|
| Formatos | CSV + TXT |
| Conflito com texto atual | Substituir tudo |
| Zero válidas | Não sobrescrever |
| Valor vs quantidade | Modo da UI |
| Modelo | CSV baixável |
| Corretora / Excel | Fora do MVP |
