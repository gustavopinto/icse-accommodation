# ICSE 2026 — Acomodações

Site para que participantes do [ICSE 2026](https://conf.researchr.org/home/icse-2026) (Rio de Janeiro) possam encontrar pessoas interessadas em compartilhar hospedagem.

> **Este site não tem nenhuma relação oficial com o evento.** É uma iniciativa individual de [Gustavo Pinto](https://gustavopinto.org).

## Funcionalidades

- Listagem pública de pedidos de acomodação
- Formulário de registro sem necessidade de cadastro (apenas e-mail válido)
- Campos: nome, e-mail, instituição, período (check-in/check-out), identidade de gênero, preferência de colega, fumante, rede social e site pessoal
- Ícone da rede social detectado automaticamente pela URL (LinkedIn, GitHub, Instagram, X, etc.)

## Stack

- **Python 3.11+** / **Flask 3**
- **Flask-SQLAlchemy** + **Flask-Migrate** (Alembic)
- **Flask-WTF** (formulários com CSRF)
- **PostgreSQL** (ex.: [Neon](https://neon.tech)); SQLite só para testes locais opcionais

## Configuração local

**1. Clonar e criar o ambiente virtual**

```bash
git clone https://github.com/gustavopinto/icse-accommodation.git
cd icse-accommodation
python -m venv .venv
source .venv/bin/activate
```

**2. Instalar dependências**

```bash
pip install -r requirements.txt
# ou requirements-dev.txt se for desenvolver
```

**3. Variáveis de ambiente**

Copie `.env.example` para `.env` e preencha. **Nunca commite o `.env`** (credenciais).

**4. PostgreSQL rodando localmente**

Se o Postgres estiver na sua máquina:

- **Criar o banco** (no terminal, com o Postgres ativo):
  ```bash
  createdb icse_accommodation
  ```
  Ou via `psql`: `CREATE DATABASE icse_accommodation;`

- No `.env`, defina a URL (troque usuário/senha se necessário):
  ```env
  DATABASE_URL=postgresql://postgres:postgres@localhost:5432/icse_accommodation
  ```
  No macOS, o usuário padrão costuma ser o do sistema; se não tiver senha, use por exemplo:
  ```env
  DATABASE_URL=postgresql://SEU_USUARIO@localhost:5432/icse_accommodation
  ```

**5. Migrar e popular o banco**

```bash
flask --app wsgi.py db upgrade
python scripts/seed.py
```

O `scripts/seed.py` cria um administrador na tabela `admins` usando `ADMIN_USERNAME` e `ADMIN_PASSWORD` do `.env` (se ainda não existir). O login do painel admin em `/admin/login` usa essa tabela.

**6. Rodar o servidor**

```bash
flask --app wsgi.py run --debug
# ou, para usar a porta 5001: flask --app wsgi.py run --debug --port 5001
```

Acesse: http://127.0.0.1:5000 (ou a porta que o Flask indicar, ex.: 5001). Painel admin: `/admin/login` (use o usuário e a senha definidos no `.env` e criados pelo seed).

## Contribuindo

Bugs e pull requests são bem-vindos em [github.com/gustavopinto/icse-accommodation](https://github.com/gustavopinto/icse-accommodation).
