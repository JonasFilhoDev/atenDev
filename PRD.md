# PRD | atenDev

Documento de requisitos do produto da primeira versão.
Gerado a partir de docs/prompt-refinado.md pelo Workflow de IA Assistida.
Este arquivo acompanha o projeto: funcionalidade nova ou correção entra como sprint nova,
com tarefas e critérios de aceite.

Ambiente de referência: Python 3.13.17, Django 6.1.3, SQLite, projeto Django `core`.
Stack de publicação: Rota A, PythonAnywhere Beginner.

---

## 1. Visão geral

Quem presta atendimento recebe pedidos por vários canais e perde a conta do que falta
fazer. O atenDev existe para responder três perguntas a qualquer momento: qual atendimento
está pendente, qual está em andamento e qual foi concluído.

Objetivo da primeira versão: um responsável entra no sistema, cadastra atendimentos,
atualiza o status, consulta a lista filtrada e mantém o histórico dos concluídos. A versão
publicada usa dados fictícios.

Fora de escopo nesta versão: vários usuários com papéis, envio de mensagem ao cliente,
pagamentos, anexos, exclusão de atendimento, relatórios e assistente de IA.

## 2. Usuários

Um único perfil, o responsável. Ele é criado pelo comando `createsuperuser` e também tem
acesso ao admin do Django. Não existe tela de cadastro de usuário e não existe recuperação
de senha nesta versão.

## 3. Requisitos funcionais

| ID | Requisito | Critério de verificação |
|---|---|---|
| RF01 | Sem autenticação, nenhuma tela de atendimento abre. | Acesso em aba anônima redireciona para a tela de login. |
| RF02 | O responsável entra com usuário e senha. | Credencial válida abre a lista; inválida mostra erro em português. |
| RF03 | O responsável sai pelo logout. | Depois do logout, voltar à lista pede login outra vez. |
| RF04 | Cadastro de atendimento com cliente, assunto e descrição. | Atendimento novo aparece na lista e sobrevive a um restart do servidor. |
| RF05 | O status começa como pendente. | Atendimento recém-criado aparece com status pendente. |
| RF06 | Edição de qualquer campo de um atendimento. | Alteração salva e visível depois de reabrir o registro. |
| RF07 | Mudança de status para em andamento ou concluído. | Status alterado persiste depois de recarregar a página. |
| RF08 | Cliente e assunto são obrigatórios. | Envio com assunto vazio é rejeitado com mensagem de erro. |
| RF09 | Lista ordenada do mais recente para o mais antigo. | Atendimento criado depois aparece no topo. |
| RF10 | Filtro da lista por status. | Filtro concluído mostra apenas os concluídos, que continuam salvos. |
| RF11 | Admin do Django disponível para o responsável. | O modelo aparece no admin com listagem e filtro por status. |

## 4. Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | Interface em português brasileiro, timezone America/Sao_Paulo. |
| RNF02 | Código em inglês, PEP 8, flake8 sem apontamento. |
| RNF03 | SECRET_KEY, DEBUG e ALLOWED_HOSTS lidos de variáveis de ambiente. |
| RNF04 | .env fora do Git, com .env.example apenas com placeholders. |
| RNF05 | Formulários validados no servidor, com mensagem de erro em português. |
| RNF06 | Regras de negócio cobertas por testes do runner do Django. |
| RNF07 | Layout simples e legível em tela de celular. |
| RNF08 | Sem exclusão de atendimento nesta versão, nem por tela nem por admin. |

## 5. Dados, regras e arquitetura

Modelo `Atendimento`, no app `atendimentos`:

| Campo | Tipo | Regra |
|---|---|---|
| cliente | CharField(120) | Obrigatório |
| assunto | CharField(160) | Obrigatório |
| descricao | TextField | Opcional |
| status | CharField com choices | pendente, em_andamento, concluido. Padrão pendente |
| created_at | DateTimeField(auto_now_add) | Automático |
| updated_at | DateTimeField(auto_now) | Automático |

Regras: ordenação padrão por `-created_at`; o status é um `TextChoices` do próprio modelo,
rotulado em português na interface; concluído não bloqueia edição.

Arquitetura: projeto `core` com `settings`, `urls` e `wsgi`; app `atendimentos` com
`models`, `forms`, `views`, `urls`, `templates/atendimentos` e `tests`. Views baseadas em
função nesta versão, com `login_required` em todas as telas de atendimento.

## 6. Interface e design system

`design_system/design-system.html` é gerado a partir do Bootstrap 5 oficial e serve de
referência para todas as telas. Telas da versão:

1. Login, em `/entrar/`.
2. Lista de atendimentos, com botões de filtro por status e link para cadastrar.
3. Formulário de cadastro e de edição, com os campos e as mensagens de erro.
4. Cabeçalho com o nome do responsável logado e o botão de sair.

A lista mostra cliente, assunto, status e data de criação. Nenhuma tela usa tabela no
celular quando a leitura ficar apertada.

## 7. Configuração local

```
cd "D:\Projetos\Projetos Pessoais\Projetos em Python\atenDev"
.\.venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py runserver
```

O `.venv` do projeto usa Python 3.13.17 e já tem Django 6.1.3 instalado. O `python` do PATH
do Windows é 3.15, por isso o ambiente do projeto não deve ser recriado com ele.

## 8. Publicação, Rota A

Pré-condição: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` vindos do
ambiente e `STATIC_ROOT` definido, o que é a Sprint 4.

1. Conta Beginner no PythonAnywhere e um console Bash no painel.
2. Clone do repositório, ambiente virtual da versão disponível na plataforma e
   `pip install -r requirements.txt`.
3. `.env` do servidor com SECRET_KEY nova, `DEBUG=False` e
   `ALLOWED_HOSTS=usuario.pythonanywhere.com`.
4. `migrate`, `collectstatic` e `createsuperuser`.
5. Aba Web com configuração manual, caminho do virtualenv, WSGI apontando para `core` e
   `/static/` mapeado para a pasta do collectstatic.
6. Repetir no endereço publicado os testes de aceite da Sprint 4, com dados fictícios.

A Rota B, VPS com Docker, fica registrada como sprint futura, fora desta versão.

## 9. Sprints

### Sprint 1 | Dados, admin e testes

- [x] Criar o app `atendimentos` e registrá-lo em `INSTALLED_APPS`.
- [x] Modelo `Atendimento` com os campos e o `TextChoices` de status.
- [x] Migração inicial.
- [x] Admin com `list_display` e `list_filter` por status.
- [x] Testes: status padrão pendente, ordenação por mais recente, filtro por status.

Critérios de aceite: um atendimento criado no admin abre de novo depois de reiniciar o
servidor; `python manage.py test` passa; o status aparece rotulado em português.

### Sprint 2 | Login, logout e proteção das páginas

- [x] Rotas `/entrar/` e `/sair/` com as views nativas do Django.
- [x] Template de login com o design system.
- [x] `login_required` nas views de atendimento e `LOGIN_URL` configurado.
- [x] Testes: anônimo é redirecionado, autenticado acessa, logout encerra a sessão.

Critérios de aceite: em aba anônima a lista não abre; depois do logout, voltar à lista pede
login de novo.

### Sprint 3 | Lista com filtro, cadastro e edição

- [x] Lista com filtro por status pela query string e estado vazio explicado na tela.
- [x] `ModelForm` com validação de cliente e assunto.
- [x] Views de cadastro e de edição, com mensagem de sucesso.
- [x] Templates das telas e navegação entre lista e formulário.
- [x] Testes: assunto vazio é rejeitado, status alterado persiste, filtro concluído mostra
      apenas concluídos.

Critérios de aceite: os caminhos válidos e inválidos são demonstráveis no navegador; a
lista continua correta depois de cadastrar, editar e filtrar.

### Sprint 4 | Preparação para publicação

- [x] `settings` lendo SECRET_KEY, DEBUG, ALLOWED_HOSTS e CSRF_TRUSTED_ORIGINS do ambiente.
- [x] `STATIC_ROOT` e `collectstatic` funcionando.
- [x] `.env.example` com placeholders e README com os passos de execução.
- [x] Verificação com `DEBUG=False` no ambiente local.

Critérios de aceite: o site abre no endereço do PythonAnywhere, os testes de aceite das
sprints anteriores passam nesse endereço e o README permite outra pessoa executar o
projeto do zero.

### Sprint 5 | Demonstração em modo leitura

- [x] Views de cadastro e de edição exigindo `atendimentos.add_atendimento` e
      `atendimentos.change_atendimento`.
- [x] Aviso em português na lista, para quem só consulta.
- [x] Botão de cadastro e link de edição escondidos de quem não tem permissão.
- [x] Testes cobrindo bloqueio de GET e de POST, HTML sem o botão, usuário com permissão e
      superusuário.
- [x] Usuário de demonstração do servidor sem as duas permissões, com a demonstração publicada
      verificada.

Critérios de aceite: com a sessão do usuário demo, `/atendimentos/novo/` e
`/atendimentos/<id>/editar/` voltam para a lista com aviso e nenhum registro é criado; o HTML da
lista do demo não traz o botão nem o link de edição; o superusuário continua cadastrando e
editando. `manage.py test` verde e flake8 limpo.

## 10. Riscos e decisões pendentes

- Acesso restrito à internet na conta gratuita do PythonAnywhere limita integração externa,
  o que está fora desta versão.
- A conta gratuita exige renovação periódica do app; a data fica no README.
- Sem exclusão de atendimento nesta versão, por decisão de escopo.
- Domínio próprio e Rota B ficam pendentes para a próxima versão.
- O repositório é público. Nenhum dado real de cliente entra nos testes nem nos exemplos.
- A demonstração publicada usa usuário `demo` sem permissão de escrita. Quem tiver a senha pode
  consultar a lista; cadastrar e editar ficam bloqueados na view e escondidos no HTML.

## 11. Checklist final de qualidade

- [ ] O pedido deste PRD e o sistema entregue descrevem a mesma versão.
- [ ] Todas as funcionalidades foram conferidas com dados fictícios.
- [ ] Os testes passam e nenhuma pendência necessária ficou aberta.
- [ ] Login, permissões e arquivos de segredo revisados.
- [ ] Código versionado no GitHub, com README e instruções de execução.
- [ ] Publicação testada no endereço público.
