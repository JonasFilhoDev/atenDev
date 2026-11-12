# atenDev

Controle de atendimentos para quem atende por vários canais e perde a conta do que falta
fazer. O sistema responde três perguntas a qualquer momento: qual atendimento está pendente,
qual está em andamento e qual foi concluído.

Primeira versão em Django 6.1 sobre Python 3.13, banco SQLite, interface em português e
timezone America/Sao_Paulo. Os dados publicados são fictícios.

## O que o sistema faz

- Login obrigatório: sem sessão, nenhuma tela de atendimento abre.
- Cadastro de atendimento com cliente, assunto e descrição. O status começa como pendente.
- Edição de qualquer campo, com mudança de status para em andamento ou concluído.
- Lista do mais recente para o mais antigo, com filtro por status pela query string.
- Admin do Django liberado para o responsável, com filtro por status.
- Não existe exclusão de atendimento nesta versão, nem pela tela nem pelo admin.

## Rotas

| Rota | Tela |
|---|---|
| `/` | Redireciona para a lista |
| `/entrar/` | Login |
| `/sair/` | Logout (POST) |
| `/atendimentos/` | Lista, com `?status=pendente`, `?status=em_andamento` ou `?status=concluido` |
| `/atendimentos/novo/` | Cadastro |
| `/atendimentos/<id>/editar/` | Edição |
| `/admin/` | Admin do Django |

## Rodar do zero

Pré-requisito: Python 3.13.

```bash
git clone https://github.com/JonasFilhoDev/atenDev.git
cd atenDev

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux e macOS
source .venv/bin/activate

pip install -r requirements.txt

# copie o modelo de variáveis e preencha a SECRET_KEY
cp .env.example .env

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Depois disso, abra `http://127.0.0.1:8000/` e entre com o usuário criado no
`createsuperuser`.

Para gerar a `SECRET_KEY` do `.env`:

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

## Variáveis de ambiente

O projeto lê o `.env` na raiz quando ele existe e, na publicação, usa as variáveis de
ambiente do servidor, que têm precedência.

| Variável | Para que serve | Exemplo |
|---|---|---|
| `SECRET_KEY` | Chave do Django. Obrigatória: sem ela o projeto não sobe. | chave gerada, longa e aleatória |
| `DEBUG` | `True` só em desenvolvimento. Em endereço público, `False`. | `False` |
| `ALLOWED_HOSTS` | Hosts aceitos, separados por vírgula. | `usuario.pythonanywhere.com` |
| `CSRF_TRUSTED_ORIGINS` | Origens confiáveis para POST, com esquema e porta. | `https://usuario.pythonanywhere.com` |

O `.env` está no `.gitignore`. O `.env.example` traz só placeholders.

## Testes e lint

```bash
python manage.py test
```

O `flake8` é ferramenta de desenvolvimento e não está no `requirements.txt`, que é o arquivo
de produção. Para rodar o lint, instale à parte e execute a partir da raiz do projeto:

```bash
pip install flake8
flake8 atendimentos core
```

## Arquivos estáticos

O Bootstrap vem por CDN, então as telas funcionam com `DEBUG=False`. O `collectstatic`
reúne o que o Django serve, como o CSS do admin:

```bash
python manage.py collectstatic
```

A pasta de destino é `staticfiles/`, já ignorada pelo Git.

## Publicação no PythonAnywhere (Rota A)

Conta Beginner, SQLite e dados fictícios.

1. Criar a conta e abrir um console Bash no painel.
2. Clonar o repositório e instalar as dependências:
   `git clone https://github.com/JonasFilhoDev/atenDev.git` seguido de
   `pip install --user -r atenDev/requirements.txt`.
3. Criar o `.env` no servidor com `SECRET_KEY` nova, `DEBUG=False`,
   `ALLOWED_HOSTS=usuario.pythonanywhere.com` e
   `CSRF_TRUSTED_ORIGINS=https://usuario.pythonanywhere.com`.
4. Rodar `python manage.py migrate`, `python manage.py collectstatic` e
   `python manage.py createsuperuser`.
5. Na aba Web, apontar o virtualenv, o `WSGI` para o `core` do projeto e mapear `/static/`
   para a pasta `staticfiles/`.
6. Repetir no endereço publicado os testes de aceite das sprints: login obrigatório, cadastro,
   edição, filtro e logout.

A conta gratuita exige renovação periódica do app. Anote a data da próxima renovação aqui:

- Próxima renovação do app gratuito: preencher na primeira publicação.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `core/` | Configuração do projeto e rotas raiz |
| `atendimentos/` | Modelo, views, formulários, testes e rotas do app |
| `templates/` | Telas, com `base.html` comum |
| `design_system/design-system.html` | Referência visual do projeto |
| `PRD.md` | Contrato da versão: requisitos, sprints e critérios de aceite |
| `docs/prompt-refinado.md` | Pedido refinado que originou o PRD |

## Escopo e dados

Repositório público. Nenhum dado real de cliente entra em exemplo, teste ou print. Ficam fora
desta versão: vários usuários com papéis, envio de mensagem ao cliente, pagamentos, anexos,
exclusão de atendimento, relatórios e assistente de IA.
