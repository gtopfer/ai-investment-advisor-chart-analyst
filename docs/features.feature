# language: pt
# Cenários BDD das specs ativas / recentes. QA e UX formalizam por feature.

Funcionalidade: SPEC-006 Harness ./devkit review estável
  Como um desenvolvedor no repositório
  Eu quero que ./devkit review passe com o venv do projeto
  Para validar lint e testes no gate do DevKit

  Cenário: pytest descobre e executa a suíte na raiz do projeto
    Dado que o ambiente de desenvolvimento do projeto está ativo
    Quando executo a suíte de testes no modo documentado do projeto
    Então todos os testes existentes passam sem erro de importação de pacotes locais

  Cenário: ruff não falha por lintar o script CLI devkit
    Dado a configuração de lint do projeto
    Quando executo o linter nos alvos de código de aplicação
    Então o script ./devkit não é tratado como código de produção a falhar o review
    E os pacotes de aplicação (analysis, allocator, ui, etc.) entram na verificação

Funcionalidade: SPEC-008 Classe BDRs removida do filtro
  Como um usuário do dashboard
  Eu quero que o multiselect de classes não ofereça BDRs
  Para não marcar uma classe sem candidatos

  Cenário: opções de classe sem BDRs
    Dado a configuração de classes de ativos da sidebar
    Quando consulto as opções disponíveis
    Então a lista contém Ações, FIIs, ETFs e Cripto
    E a lista não contém BDRs

  Cenário: ticker BDR na carteira não é rejeitado só por ser BDR
    Dado uma linha de carteira com ticker no formato BDR (ex.: AAPL34.SA, valor positivo)
    Quando o parse da carteira atual é executado
    Então o ticker entra no mapa de posições
