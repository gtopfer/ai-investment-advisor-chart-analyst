# Skill: Code Review (programático + manual)

> **Usado por**: Developer (antes de sair de `test_red`); QA (fase `code_review`); qualquer um que rode `./devkit review`.  
> **Gate do kit**: sem esta skill cumprida, **não** há `./devkit approve` em `test_red` → `code_review`.

## Quando usar

- Sempre ao final da implementação.  
- Sempre na validação QA.  
- Após refactors grandes no loop autônomo.

## Parte A — Validação automatizada (obrigatória)

Na **raiz do repositório**:

```bash
./devkit review
```

O comando deve terminar com **APROVADO** e código de saída `0`.

Ele tipicamente verifica:

| Check | Significado |
|-------|-------------|
| TODO/FIXME em comentários de código | Trabalho incompleto proibido |
| Linter / `py_compile` / equivalente | Estilo e sintaxe |
| Typecheck / build | Tipos e compilação |
| Suíte de testes | Comportamento |

### Se REPROVADO

1. Leia o trecho de log (não chute).  
2. Corrija a causa raiz no arquivo certo.  
3. Rode `./devkit review` de novo.  
4. Integre com `.ai/skills/autonomous-loop.md` (máx. 3 tentativas na mesma causa).

**Não** rode `./devkit approve` com review vermelho.

## Parte B — Revisão manual do diff (obrigatória)

Olhe o diff dos arquivos da feature (`git diff` / status). Checklist:

### Correção & escopo

- [ ] Atende aos requisitos da spec ativa (nada a menos crítico; nada a mais oportunista)
- [ ] Não quebra contratos do `technical-spec.md`
- [ ] Edge cases citados na spec tratados ou explicitamente fora de escopo

### Design & clareza

- [ ] Nomes legíveis; funções curtas; responsabilidade única
- [ ] Sem duplicação gritante (DRY com juízo)
- [ ] Sem “código morto”, prints de debug ou comentários óbvios
- [ ] Camadas respeitadas (domain sem infra; UI sem SQL direto)

### Segurança & dados

- [ ] Sem segredos, tokens, senhas ou chaves no código
- [ ] Inputs externos validados na borda
- [ ] Auth/autorização respeitada se a spec exige
- [ ] Logs não vazam PII sensível

### Testes

- [ ] Testes da feature existem e passam
- [ ] Não há `skip` injustificado
- [ ] Mocks nas dependências externas

### Completude

- [ ] Sem `// TODO`, `// FIXME`, `// o resto do código…`
- [ ] Mensagens de erro úteis ao usuário/sistema
- [ ] Migrações/config documentadas se a feature exige

## Parte C — Veredito

| Resultado | Quem | Ação |
|-----------|------|------|
| APROVADO (A+B) | Developer | `./devkit approve` → QA |
| REPROVADO (A ou B) | Developer | Corrigir ou escalar |
| APROVADO (A+B) | QA | `./devkit approve` → PM DoD |
| REPROVADO | QA | `./devkit reject` → Developer |

## Anti-padrões

- Confiar só no linter e ignorar o diff  
- Aprovar com warning de teste flaky “às vezes passa”  
- Deixar TODO “para depois”  
- Review de 500 arquivos: peça para fatiar a feature  

## Saída sugerida no chat

```text
[Code Review] APROVADO | REPROVADO
CLI: ./devkit review → ...
Manual: N itens ok / lista de achados
```
