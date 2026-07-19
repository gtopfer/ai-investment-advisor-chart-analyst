# Skill: Checklist de Code Review Programático

Esta skill define o processo de garantia de qualidade de código. Ela deve ser executada obrigatoriamente pelo desenvolvedor antes de encerrar o desenvolvimento.

## 1. Validação Automatizada (CLI)
A primeira e mais importante etapa do code review é executar a validação estática programática do projeto.
- **Comando Obrigatório**: RODE `./devkit review` na raiz do projeto.
- Este comando detectará automaticamente a stack do projeto, executará o linter, o typecheck e rodará a suíte de testes do projeto, além de fazer uma varredura em busca de comentários `TODO` ou `FIXME` e trechos de código incompletos.

## 2. Critérios de Avaliação
O code review é considerado **APROVADO** apenas se a saída de `./devkit review` retornar sucesso (saída 0) e sem violações. Se o comando reportar falha, o desenvolvedor deve:
1. Ler o log de erros produzido pela CLI.
2. Corrigir as falhas diretamente no código.
3. Executar `./devkit review` novamente até obter sucesso absoluto.

## 3. Revisão Manual (Auto-Revisão)
Além da validação automatizada, o desenvolvedor deve fazer uma leitura atenta no git diff para assegurar:
- **Clean Code**: SOLID, DRY, nomes de variáveis legíveis, documentações claras.
- **Segurança**: Nenhuma credencial, token ou chave de API salva diretamente no código (hardcoded). Todos os segredos devem vir de variáveis de ambiente.
- **Sem Placeholders**: Sem comentários desnecessários explicando lógica trivial ou código órfão esquecido.
