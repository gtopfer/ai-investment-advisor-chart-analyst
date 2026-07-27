# Especificação de Feature: Configuração Inicial

## 1. Contexto & Valor de Negócio
- **Como um(a)** desenvolvedor(a) ou time que usa assistentes de IA para codar
- **Eu quero** uma estrutura DevKit-AI pronta na raiz do repositório
- **Para que** o fluxo spec-driven (PM → Architect → QA → Developer) e a CLI `./devkit` estejam disponíveis desde o primeiro dia

## 2. Requisitos & Restrições
- Requisito 1: Existir o diretório `.ai/` com instruções globais, state tracker, template de specs, technical-spec, agents, skills, guidelines e pasta `specs/`
- Requisito 2: Existir a CLI executável `./devkit` com `init`, `propose`, `hotfix`, `status`, `sync`, `activate`, `approve`, `reject`, `review`, `doctor`, `log` e `help`
- Requisito 3: Existir pontos de entrada de contexto para IAs (`CLAUDE.md`, `GEMINI.md`) apontando para a rotina de inicialização
- Requisito 4: Existir `docs/README.md` e `docs/CHANGELOG.md` para documentação de entregas
- Requisito 5: A stack de produto do app-alvo permanece `_(a definir)_` até a primeira feature real passar pelo Architect
- Restrição 1: Este setup não cria `src/`, `backend/`, `frontend/` nem escolhe framework de aplicação

## 3. Expectativas de UI/UX (se aplicável)
- Não aplicável (infraestrutura de processo e CLI, sem interface de produto)

## 4. Checklist Técnico / Notas
- Precisa de mudança no banco de dados: Não
- Novos pacotes/dependências: Não (CLI em Python 3 da stdlib)
- Regras de segurança/permissão: N/A

## 5. Definition of Ready (DoR — Pronto para Começar)
- [x] O problema de negócio e o resultado desejado estão claros
- [x] Dependências externas (APIs, credenciais, dados) estão disponíveis ou explicitamente adiadas
- [x] Perguntas em aberto foram respondidas por quem pediu

## 6. Definition of Done (DoD — Pronto/Concluído)
- [x] Todos os requisitos da seção 2 estão atendidos
- [x] Os critérios de aceitação (estrutura e comandos da CLI) são verificáveis no repositório
- [x] Documentação atualizada: entrada em `docs/CHANGELOG.md`
- [x] Nenhuma regressão conhecida em funcionalidades adjacentes
