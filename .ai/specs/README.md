# Pasta de Especificações (.ai/specs/)

Esta pasta é o local central onde você deve depositar e atualizar os arquivos de especificação (`.md`) das suas features ou correções.

## Regras de Organização
1. **Nomeação**: Nomeie os arquivos começando com um prefixo numérico ou identificador claro.
   - Exemplo: `001_filtro_status.md`, `002_corrigir_login.md`.
2. **Ciclo de Vida Automático**: A IA lerá esta pasta no início de cada interação e atualizará o arquivo `.ai/state.md` com o status de cada especificação.
3. **Formato Sugerido**: As especificações criadas aqui devem seguir o molde do arquivo `.ai/template.specs`.

## Como adicionar uma nova especificação
Basta criar um arquivo markdown nesta pasta (ex: `.ai/specs/003_minha_feature.md`) e escrever em linguagem simples o que você precisa. Na próxima interação, a IA detectará o novo arquivo, registrará em `.ai/state.md` com status `draft` e iniciará o fluxo a partir do papel de PM.
