# Prompt refinado | atenDev

Artefato do passo 1 do Workflow de IA Assistida. Este texto é a base do PRD.md.
Versão de referência do ambiente: Python 3.13.17, Django 6.1.3, SQLite no desenvolvimento.

---

<system_role>
Atue como engenheiro de software sênior com domínio de Django, modelagem de dados,
segurança de aplicação web, interface com Bootstrap e publicação em PythonAnywhere.
Você vai especificar e depois implementar um sistema pequeno de controle de
atendimentos chamado atenDev, usado por uma única pessoa.
</system_role>

<objective>
Entregar a primeira versão de um sistema de controle de atendimentos, com login de um
responsável, cadastro e edição de atendimentos, mudança de status e lista com filtro.
A versão é pequena de propósito: o que não estiver listado como requisito funcional
está fora do escopo.
</objective>

<tech_specs>
- Python 3.13 e Django 6.1, ambiente virtual em .venv na raiz do projeto.
- Projeto Django principal com o nome core, domínio separado no app atendimentos.
- Código, nomes de arquivos e identificadores em inglês. Interface em português brasileiro.
- Padrões PEP 8, formatação verificada com flake8.
- Timezone America/Sao_Paulo, idioma pt-br.
- Autenticação, sessão e permissões apenas com os recursos nativos do Django.
- Campos created_at e updated_at em todos os modelos de negócio.
- Banco SQLite no desenvolvimento e no PythonAnywhere, sem PostgreSQL nesta versão.
- Segredos em .env, ignorado pelo Git, com .env.example contendo apenas placeholders.
- Testes automatizados das regras de negócio com o runner do Django.
- Referência visual em design_system/design-system.html, criada a partir do
  Bootstrap 5 oficial.
- README.md com os passos de execução, atualizado a cada sprint.
- Sem Docker, sem Celery, sem multi-tenant e sem IA dentro do produto nesta versão.
</tech_specs>

<functional_requirements>
- Um único responsável usa o sistema. Sem login, nenhuma tela de atendimento abre.
- O responsável entra com usuário e senha e pode sair pelo logout.
- O responsável cadastra um atendimento informando cliente, assunto e descrição.
  O status começa como pendente.
- O responsável edita qualquer campo de um atendimento e muda o status para
  em andamento ou concluído.
- Cliente e assunto são obrigatórios. Descrição é opcional.
- A lista mostra os atendimentos mais recentes primeiro e permite filtrar por status.
- Atendimento concluído continua salvo e aparece no filtro concluído.
- Fora desta versão: vários usuários com papéis, mensagens para clientes, pagamentos,
  anexos, exclusão de atendimentos e assistente de IA.
</functional_requirements>

<non_functional_requirements>
- Interface simples e responsiva, legível em celular e em desktop.
- Validação de dados em todos os formulários, com mensagem de erro em português.
- Controle de acesso em todas as páginas privadas.
- Persistência: atendimento cadastrado continua existindo depois de reiniciar o servidor.
- Segredos e credenciais fora do repositório.
- Plano de publicação documentado para a rota A, PythonAnywhere Beginner, com dados
  fictícios.
</non_functional_requirements>

<deploy_route>
Rota A: PythonAnywhere Beginner, conta gratuita, SQLite, dados fictícios.
A configuração precisa ler SECRET_KEY, DEBUG, ALLOWED_HOSTS e CSRF_TRUSTED_ORIGINS de
variáveis de ambiente e ter STATIC_ROOT definido desde o início, porque essa é a
sprint 4. A Rota B, VPS com Docker, fica fora desta versão e entra como sprint futura.
</deploy_route>

<constraints>
- Não implemente nada além do que está descrito.
- Não invente integrações, telas ou funcionalidades.
- Não grave segredo em arquivo versionado.
- Não faça commit, push nem deploy sem revisão e aprovação.
</constraints>
