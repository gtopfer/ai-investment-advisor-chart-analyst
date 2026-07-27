# Git hooks (opcional)

| Arquivo | Função |
|---------|--------|
| `pre-commit` | Executa `./devkit review` antes do commit |

## Instalação local

```bash
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Não é instalado automaticamente pelo `./devkit init` (evita surpresa em monorepos). Documente no README do app se o time adotar.
