# Skill: Loop de Execução Autônoma e Autocorreção

Este protocolo descreve a rotina de desenvolvimento e depuração iterativa de código para implementar a funcionalidade com o menor nível de ruído possível.

## 1. O Ciclo do Loop
Quando estiver na fase de desenvolvimento (`test_red`), siga o fluxo:

```
1. PLANEJAR   ➔ Leia .ai/specs/<spec>.md e verifique quais arquivos precisam ser tocados.
2. ESCREVER   ➔ Implemente a mudança no código (seguindo o princípio TDD).
3. EXECUTAR   ➔ Rode ./devkit review para validar linter, typecheck, testes e TODOs de uma só vez.
4. AVALIAR    ➔ Se o resultado for APROVADO, avance. Se for REPROVADO, leia o erro.
5. REFATORAR  ➔ Limpe e organize o código novo. Execute `./devkit review` novamente após refatorar.
```

## 2. Autocorreção (Self-Healing)
Se o comando `./devkit review` indicar falhas (linter quebrando, testes falhando, typecheck incorreto):
1. **Identifique a causa raiz**: Não tente adivinhar. Leia a stack trace impressa pela CLI.
2. **Correção Direta**: Corrija o arquivo fonte associado ao erro.
3. **Loop de Re-verificação**: Execute `./devkit review` novamente. Uma correção só é considerada válida após passar pelo crivo da CLI.

## 3. Condições de Parada (Esgotamento)
Para evitar que a IA entre em loops infinitos consumindo tokens desnecessariamente, pare a execução e solicite ajuda do usuário se:
- **3 tentativas consecutivas** de correção da mesma causa raiz falharem.
- A correção exigir novas dependências de pacotes não previstas na especificação.
- Houver falha de infraestrutura externa (ex: credencial de API ausente, banco de dados local inacessível).

Ao escalar para o usuário, relate claramente:
1. O que foi tentado.
2. Os logs de erro das tentativas falhas.
3. A decisão ou informação específica necessária para prosseguir.
