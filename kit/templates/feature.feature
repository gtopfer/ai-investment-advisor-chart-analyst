# language: pt

Funcionalidade: [Resumo da feature]
  Como [persona/tipo de usuário]
  Quero [ação/capacidade]
  Para que [valor/resultado esperado]

  Contexto:
    Dado que [estado inicial / condição pré-estabelecida]
    E [outra condição se houver]

  Cenário: [Happy path - descrição concreta do que o usuário vê/faz]
    Quando [ação principal]
    E [passo 2]
    Então [resultado observável]
    E [outra observação]

  Cenário: [Falha crítica - o que acontece se der errado]
    Quando [ação que falha]
    Então [mensagem de erro ou estado de fallback]
    E [usuário pode retry ou continuar]

  Cenário: [Edge case 1]
    Quando [situação limite]
    Então [comportamento esperado na borda]

  Cenário: [Edge case 2]
    Quando [outra situação limite]
    Então [comportamento esperado]

---

## Exemplos de Features Bem Escritas

### Exemplo 1: Login com SSO

```gherkin
# language: pt

Funcionalidade: Autenticação via SSO
  Como usuário corporativo
  Quero fazer login com minha conta corporativa
  Para acessar a plataforma sem criar senha extra

  Contexto:
    Dado que o servidor de SSO está online
    E que meu email corporativo é registrado no provedor

  Cenário: Login bem-sucedido via SSO
    Quando clico no botão "Entrar com SSO"
    E sou redirecionado para o login corporativo
    E insiro meu email e senha corporativos
    Então sou redirecionado de volta à plataforma
    E estou autenticado (vejo meu nome no menu)
    E cookies de sessão estão presentes

  Cenário: Login falha se email não está registrado
    Quando clico no botão "Entrar com SSO"
    E sou redirecionado para o login corporativo
    E tento usar um email não corporativo
    Então vejo mensagem "Email não autorizado"
    E NÃO sou redirecionado de volta
    E nenhuma sessão é criada

  Cenário: Session expirada durante fluxo de SSO
    Quando inicio o fluxo de login
    E a sessão temporária expira antes de confirmar
    Então vejo erro "Link expirou"
    E posso clicar "Tentar Novamente"
```

### Exemplo 2: Exportação de Relatório

```gherkin
# language: pt

Funcionalidade: Exportar Relatório em CSV
  Como administrador de loja
  Quero exportar um relatório de vendas
  Para analisar dados em Excel

  Contexto:
    Dado que estou logado
    E que há pelo menos 1 relatório salvo

  Cenário: Exportar relatório com dados completos
    Quando clico em "Exportar" em um relatório
    E confirmo a exportação no modal
    Então um arquivo CSV é baixado
    E o arquivo contém cabeçalhos da tabela
    E o arquivo contém todas as 500 linhas de dados

  Cenário: Exportação cancelada
    Quando clico em "Exportar"
    E clico "Cancelar" no modal
    Então nenhum arquivo é baixado
    E continuo na página do relatório

  Cenário: Erro se servidor está lento (timeout)
    Quando clico em "Exportar"
    E o servidor demora > 30s para processar
    Então vejo spinner/loading
    E após 30s vejo "Exportação falhou. Tente novamente."
    E posso clicar "Tentar Novamente"
```

---

## Checklist para Gherkin Bom

- [ ] **Linguagem clara** — um QA/PM não-técnico entende sem glossário
- [ ] **Concreto** — nomes, dados, estados reais; sem placeholders `[...]`
- [ ] **Comportamento observável** — "o usuário vê X", "arquivo é baixado", não "código faz Y"
- [ ] **Um pré-requisito por linha** (Dado/E) — não aglomere
- [ ] **Uma ação por cenário** (Quando) — não 10 passos
- [ ] **Resultado claro** (Então) — não "funciona"
- [ ] **Happy path + ≥ 1 falha + ≥ 1 borda** — mínimo 3 cenários por feature

---

## Dicas

1. **Escreva como se fosse reportar um bug:** "Quando clico X, esperava Y, mas vi Z"
2. **Use "Dado" para estado inicial, não para instruções de setup:** "Dado que há 3 itens no carrinho" (bom) vs "Dado que abro o app e clico em itens" (ruim)
3. **Uma sentença = um pré-requisito:** se precisar de "E" mais de 2x, o cenário é grande demais
4. **Teste sempre contra a UI/resultado observável:** nunca "dado que a função X foi chamada"

---

**Próximo:** Este arquivo é lido por QA (escreve testes) e Developer (implementa). Mantenha legível.
