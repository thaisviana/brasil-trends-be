# trends-brasil-be
Understanding Brasil election through Google Trends Data

## Pré-requisitos

- **Python 3.6+** (O projeto especifica 3.6.5, mas versões mais recentes do 3.x geralmente funcionam)
- **PostgreSQL**

## Instalação

1. Clone o repositório e entre na pasta do projeto:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd brasil-trends-be
   ```

2. Acesse o diretório da aplicação:
   ```bash
   cd trendsApi
   ```

3. Crie um ambiente virtual e ative-o:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # ou
   .venv\Scripts\activate  # Windows
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração

1. Crie um arquivo `.env` dentro da pasta `trendsApi` (onde está o `manage.py`) com as seguintes variáveis:

   ```env
   SECRET_KEY='sua-chave-secreta-segura'
   DEBUG=True
   DATABASE_URL=postgres://usuario:senha@localhost:5432/nome_do_banco
   ```

   > **Nota:** Ajuste a `DATABASE_URL` com seu usuário, senha e nome do banco de dados PostgreSQL local.

## Banco de Dados

1. Certifique-se de que o PostgreSQL está rodando e crie o banco de dados (se ainda não existir):
   ```bash
   createdb nome_do_banco
   ```

2. Execute as migrações para criar as tabelas:
   ```bash
   python manage.py migrate
   ```

## Rodando o Projeto

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O projeto estará acessível em [http://localhost:8000](http://localhost:8000).
