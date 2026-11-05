# ATV09 — Migração do Portal para Django

## Identificação da dupla

- Gabriel Barbosa da Silva — Turma 513
- Eduardo Joaquim Santos da Silva — Turma 513

Curso Técnico em Informática — IFAL, Campus Palmeira dos Índios.

## Descrição do projeto

Este projeto é a evolução do portal unificado feito nas atividades anteriores (ATV05, ATV06 e ATV07).
O portal, que antes era um site feito só com HTML, CSS e JavaScript, foi migrado para o **Django**.

O que mudou:

- Os conteúdos (currículos, temas, página inicial e contato) agora ficam **guardados no banco de dados**, no Model `Conteudo`, e o HTML interno de cada página é cadastrado pelo Django Admin.
- O menu é **gerado dinamicamente** a partir do Model `Menu`. Cada item aponta para um `Conteudo` (link interno) ou para uma URL (link externo).
- A navegação usa as **URLs e Views do Django** (`/` e `/conteudo/<slug>/`), e não mais JavaScript.
- A estrutura do portal (`header`, `nav`, `main`, `footer`) ficou em um **template base** com herança de templates.
- CSS, imagens e JavaScript ficam como **arquivos estáticos** do app.
- Foi mantida a identidade visual, o layout com Grid/Flexbox e a responsividade da ATV06/ATV07.
- O formulário de Contato / Ouvidoria da ATV07 foi mantido (validação do navegador + `confirm()` em JavaScript + página de confirmação feita por uma View).

### Models

| Model | Campos principais |
|-------|-------------------|
| `Conteudo` | `titulo`, `slug` (único), `conteudo_html`, `ativo` |
| `Menu` | `titulo`, `tipo_destino` (interno ou externo), `ordem`, `ativo`, `conteudo` (ForeignKey para `Conteudo`, usado no destino interno), `url_externa` (usada no destino externo) |

### URLs

| URL | Descrição |
|-----|-----------|
| `/` | Página inicial (conteúdo com slug `inicio`) |
| `/conteudo/<slug>/` | Mostra o conteúdo cujo slug vem na URL. Ex.: `/conteudo/tema-dr-stone/` |
| `/mensagem-enviada/` | Página de confirmação do formulário de contato |
| `/admin/` | Django Admin |

### Dados iniciais

O arquivo `portal/fixtures/dados_iniciais.json` cadastra:

- 1 página inicial + 5 outros conteúdos internos (Currículo - Gabriel, Tema: God of War 2, Currículo - Eduardo, Tema: Dr. Stone, Contato / Ouvidoria);
- 3 links externos (GitHub - Gabriel, GitHub - Eduardo e W3Schools);
- 9 itens de menu (6 internos e 3 externos).

## Tecnologias utilizadas

- Python 3
- Django 5.2
- SQLite (banco de dados padrão do Django)
- HTML5 semântico, CSS3 (Grid, Flexbox e Media Queries) e JavaScript
- Git e GitHub

## Como executar o projeto

Todos os comandos abaixo são executados dentro da pasta do projeto (a pasta onde está o arquivo `manage.py`).

### 1. Criar e ativar o ambiente virtual

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Executar as migrations

```bash
python manage.py migrate
```

### 4. Carregar os dados iniciais (conteúdos e menu)

```bash
python manage.py loaddata dados_iniciais
```

### 5. Criar o superusuário

```bash
python manage.py createsuperuser
```

Informe um nome de usuário, e-mail (pode deixar em branco) e senha.

### 6. Executar o servidor

```bash
python manage.py runserver
```

### 7. Acessar a aplicação

- Portal: http://127.0.0.1:8000/
- Django Admin: http://127.0.0.1:8000/admin/ (entre com o superusuário criado no passo 5)

No Django Admin, em **Conteúdos** e **Itens do menu**, é possível cadastrar, alterar, excluir, ativar/desativar e reordenar. As alterações aparecem no portal na hora.

### Testes automáticos (opcional)

```bash
python manage.py test
```

## Estrutura do projeto

```
ATV09_GABRIEL_EDUARDO/
├── manage.py
├── requirements.txt
├── config/                  # Projeto Django (settings, urls)
└── portal/                  # Aplicação Django
    ├── models.py            # Conteudo e Menu
    ├── admin.py             # Registro dos Models no Admin
    ├── views.py             # pagina_inicial, exibir_conteudo, mensagem_enviada e obter_itens_menu
    ├── urls.py
    ├── migrations/
    ├── fixtures/dados_iniciais.json
    ├── templates/portal/    # base.html, conteudo.html, mensagem_enviada.html
    └── static/portal/       # css/, img/, js/ e docs/
```
