# Estado do Desenvolvimento (Task Tracker)

Este arquivo é lido e atualizado automaticamente pela IA para rastrear o status de cada especificação no diretório `.ai/specs/` e gerenciar a transição de fases.

## Como funciona
1. **Rastreamento Automático**: A IA verifica os arquivos na pasta `.ai/specs/` e atualiza a tabela abaixo com o status correspondente.
2. **Ciclo de Vida (Fases)**:
   - `draft` (Rascunho inicial do PM)
   - `spec_approved` (Requisitos de negócio aprovados pelo usuário; aguardando arquitetura)
   - `tech_approved` (Especificação técnica aprovada pelo usuário; aguardando testes)
   - `test_red` (Testes TDD escritos e falhando; aguardando implementação)
   - `code_review` (Implementado; passando por revisão estática)
   - `tested` (Testes passando com sucesso; aguardando validação do DoD pelo PM)
   - `done` (Entregue, documentado e concluído)

---

## Lista de Especificações Ativas

| Código | Título da Spec | Caminho do Arquivo | Status Atual | Próxima Fase | Última Atualização |
|--------|----------------|-------------------|--------------|--------------|---------------------|
| SPEC-000 | Configuração Inicial | `.ai/specs/000_setup.md` | `done` | `done` | 2026-07-18 |

---

## Histórico de Execuções Recentes

* **2026-07-18**: Inicialização do repositório devkit-ai.
