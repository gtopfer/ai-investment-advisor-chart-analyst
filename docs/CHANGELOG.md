# Changelog

Todas as mudanças notáveis deste projeto são documentadas aqui. O formato segue livremente o [Keep a Changelog](https://keepachangelog.com/).

Cada entrada deve descrever impacto (o que mudou para usuários/sistema), não detalhe de implementação.

## [Não Lançado]

### Adicionado
- **SPEC-005**: Suporte completo a cripto — lista ampliada, normalização `BTC`→`BTC-USD`, score só técnico (sem penalizar DY=0), preços em USD com aviso de moeda mista.
- **SPEC-001**: Módulo multi-LLM — escolha de provedor Groq ou OpenAI-compatible (Ollama, OpenRouter, etc.), modelo editável na sidebar, chaves via env.
- **SPEC-002**: Layout escuro minimalista — sidebar em seções colapsáveis, empty state guiado, cards de resumo, menos ruído visual.
- **SPEC-003**: Importar carteira atual via CSV/TXT, com modelo baixável e substituição da carteira na sessão.
- **SPEC-004**: Visão **“Como deve ficar”** (atual vs projetado) e botão para aplicar a projeção na carteira da sessão.
- Estrutura inicial do projeto (Dev ToolKit)

### Alterado
- Análise de IA desacoplada do SDK Groq via pacote `llm/`.
- Documentação de configuração (`.env.example`, README) para novos provedores e variáveis.
