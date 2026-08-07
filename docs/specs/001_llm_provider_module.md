# Especificação de Feature: Módulo multi-LLM (provedor configurável)

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário(a) do dashboard de análise de investimentos
- **Eu quero** escolher e configurar o provedor de LLM de minha preferência (não só Groq)
- **Para que** a interpretação técnica dos gráficos use o modelo/provedor que eu já tenho acesso, custo e qualidade desejados — sem depender de um único fornecedor

## 2. Requisitos & Restrições

### Requisitos funcionais
1. **Módulo de provedores**: existe uma camada com interface comum para “gerar análise técnica via LLM”, desacoplada do restante do pipeline (scoring, alocação, UI de carteira).
2. **Provedores do MVP**:
   - **Groq** (compatibilidade com o comportamento atual e `GROQ_API_KEY`).
   - **OpenAI-compatible** (cliente com `base_url` + `api_key` + `model`), cobrindo Ollama, OpenRouter, LM Studio, vLLM, proxies OpenAI, etc.
3. **Seleção na UI**: na sidebar (bloco de IA / Avançado), o usuário escolhe o **provedor ativo** e o **modelo** entre as opções habilitadas.
4. **Configuração híbrida (env + UI)**:
   - Credenciais e defaults vêm de variáveis de ambiente / `.env` (documentadas em `.env.example`).
   - A UI lista apenas provedores **com configuração mínima detectada** (ex.: chave presente; no caso OpenAI-compatible, chave e/ou base_url conforme regra definida na fase técnica).
   - Preferência de provedor/modelo da sessão fica em **session state** do Streamlit (sem banco).
5. **Modelo editável**: cada provedor tem um **default sensato** (env ou fallback hardcoded); o usuário pode **sobrescrever o nome do modelo** na sidebar para a sessão.
6. **Contrato de saída inalterado**: o resultado da análise continua no formato atual (`trend`, `short_summary_pt`, `confidence_score`, `support_levels`, `resistance_levels` — `AIAnalysisResult`). O módulo abstrai transporte/SDK, não a regra de negócio do score.
7. **Fallback gracioso**: sem credencial, provedor indisponível ou erro de API → app não quebra; retorna análise neutra com mensagem clara em PT-BR citando o provedor tentado.
8. **Limites de segurança existentes**: `AI_ACCESS_PASSWORD` e `MAX_AI_CALLS_PER_SESSION` continuam válidos **independente** do provedor escolhido.
9. **Retrocompatibilidade**: instalação que só define `GROQ_API_KEY` (como hoje) continua funcionando sem exigir novas variáveis obrigatórias; Groq permanece o default quando for o único provedor configurado.
10. **Rotulagem da UI**: o checkbox deixa de dizer só “Groq”; passa a linguagem genérica (“Rodar análise IA” / equivalente), indicando o provedor ativo quando relevante.

### Restrições
1. **Sem persistência** de chaves ou preferências em banco/arquivo de usuário no repo.
2. **Escopo**: apenas a análise técnica de chart/IA do produto — não é um chat multi-turno genérico.
3. **MVP enxuto de dependências**: nativo Groq + cliente OpenAI-compatible; **não** incluir SDKs Anthropic/Gemini nativos neste ciclo (podem ser specs futuras).
4. **Sem expor segredos na UI**: nunca renderizar a API key completa; no máximo “chave detectada / não detectada”.

## 3. Expectativas de UI/UX

- **Sidebar → bloco de IA (Avançado)**:
  - Checkbox: “Rodar análise IA” (sem amarrar o texto a um único vendor).
  - Selectbox **Provedor** (ex.: Groq, OpenAI-compatible) — só opções habilitadas pela config.
  - Campo **Modelo** (texto editável) pré-preenchido com o default do provedor selecionado; troca de provedor atualiza o default se o usuário não tiver customizado (comportamento detalhável na fase técnica).
  - Caption/status: “Chave detectada” / “Config incompleta” sem revelar o segredo.
- Se nenhum provedor estiver configurado e o usuário ativar a IA: aviso claro de que a análise IA ficará indisponível (fallback).
- Tabela de carteira, rebalanceamento e demais seções **sem mudança de layout**.
- Mensagens de erro/fallback em PT-BR, mencionando o provedor (ex.: “Erro ao conectar com o motor de IA (OpenAI-compatible).”).

## 4. Checklist Técnico / Notas
- Precisa de mudança no banco de dados: **Não**
- Novos pacotes/dependências: **Provável** — cliente OpenAI-compatible (ex. pacote `openai` ou HTTP fino); manter `groq` para o adapter nativo. Decisão final na fase Architect.
- Regras de segurança/permissão: senha opcional de IA + limite de calls/sessão; chaves só via env.
- Variáveis de ambiente candidatas (Architect pode renomear/consolidar):
  - Existentes: `GROQ_API_KEY`, `AI_ACCESS_PASSWORD`, `MAX_AI_CALLS_PER_SESSION`
  - Novas (exemplo): `LLM_PROVIDER` (default), `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `OPENAI_MODEL`, `GROQ_MODEL` (ou unificar `LLM_MODEL` por provedor)
- Orientação de desenho (não prescreve pastas finais): interface de provider + implementações Groq e OpenAI-compatible; `ai_chart_engine` orquestra prompt/parse e delega a chamada.

## 5. Definition of Ready (DoR — Pronto para Começar)
- [x] O problema de negócio e o resultado desejado estão claros
- [x] Lista de provedores do MVP definida: **Groq + OpenAI-compatible**
- [x] Configuração: **env + seletor na sidebar**
- [x] Modelo: **editável na UI com default sensato**
- [x] Dependências externas: chaves opcionais; feature degrada sem elas
- [x] Perguntas em aberto do solicitante respondidas (2026-07-26)

## 6. Definition of Done (DoD — Pronto/Concluído)
- [x] Todos os requisitos da seção 2 estão atendidos
- [x] Com `GROQ_API_KEY`, a análise IA via Groq funciona como antes (ou equivalente observável)
- [x] Com config OpenAI-compatible válida, a mesma análise roda por esse provedor
- [x] Usuário consegue trocar provedor/modelo na sidebar na sessão
- [x] Sem chave / erro de API: fallback gracioso, app não quebra
- [x] Senha de IA e limite de calls/sessão ainda se aplicam a qualquer provedor
- [x] Critérios de aceitação (Gherkin abaixo / `.ai/features.feature`) cobertos por testes automatizados
- [x] Documentação: `docs/CHANGELOG.md`, README e `.env.example` atualizados; ADR/decisão na seção 9 de `.ai/technical-spec.md` se aplicável
- [x] Nenhuma regressão conhecida em scoring, alocação e rebalanceamento

## 7. Critérios de aceitação (rascunho Gherkin — QA/BDD formalizará)

```gherkin
# language: pt
Funcionalidade: Provedor LLM configurável na análise de gráficos

  Cenário: Análise via Groq com configuração legada
    Dado que apenas GROQ_API_KEY está configurada
    E a análise IA está ativada com provedor Groq
    Quando o usuário gera a carteira recomendada
    Então os ativos processados pela IA recebem resumo em PT-BR ou fallback neutro sem quebrar o app

  Cenário: Análise via endpoint OpenAI-compatible
    Dado que base_url e api_key OpenAI-compatible estão configuradas
    E o usuário seleciona o provedor OpenAI-compatible e um modelo
    Quando a análise IA é executada
    Então a chamada usa esse provedor/modelo e o resultado respeita o contrato AIAnalysisResult

  Cenário: Fallback sem credenciais
    Dado que nenhum provedor tem credencial válida
    Quando o usuário ativa a análise IA e gera a carteira
    Então o app conclui a análise sem erro fatal
    E a mensagem indica que a IA está indisponível

  Cenário: Limite de calls por sessão
    Dado que o limite MAX_AI_CALLS_PER_SESSION foi atingido
    Quando o usuário tenta nova rodada com IA
    Então novas chamadas LLM não são feitas independentemente do provedor
```

## 8. Decisões de produto fechadas (PM)
| Decisão | Valor |
|---------|--------|
| MVP providers | Groq + OpenAI-compatible |
| Config | Env (chaves/defaults) + seletor na sidebar |
| Modelo | Editável com default sensato |
| Fora do MVP | SDKs nativos Anthropic/Gemini; chat multi-turno; persistência de preferências |
