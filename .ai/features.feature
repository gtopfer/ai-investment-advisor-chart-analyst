# language: pt
# Nota: o Gherkin tem suporte nativo a português — a diretiva "# language: pt" ativa
# as palavras-chave Funcionalidade/Cenário/Dado/Quando/Então/E abaixo. Não é uma
# tradução informal: é sintaxe reconhecida pelas ferramentas de BDD (Cucumber, Behave etc).

Funcionalidade: Autenticação de Usuário

  Como um usuário registrado
  Eu quero fazer login com minhas credenciais
  Para que eu possa acessar meu painel privado

  Contexto:
    Dado que a aplicação está rodando
    E o banco de usuários está populado com um usuário de teste "usuario@exemplo.com" com senha "SenhaSegura123"

  Cenário: Login bem-sucedido com credenciais válidas
    Dado que estou na página de login
    Quando eu preencho o campo de e-mail com "usuario@exemplo.com"
    E preencho o campo de senha com "SenhaSegura123"
    E clico no botão de login
    Então devo ser redirecionado para a página do painel
    E devo ver uma mensagem de boas-vindas "Bem-vindo de volta, usuario@exemplo.com"

  Cenário: Login falho com senha inválida
    Dado que estou na página de login
    Quando eu preencho o campo de e-mail com "usuario@exemplo.com"
    E preencho o campo de senha com "SenhaErrada"
    E clico no botão de login
    Então devo ver uma mensagem de erro "Credenciais inválidas"
    E devo permanecer na página de login
