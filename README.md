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

```env
FLASK_ENV=development
SECRET_KEY=troque-por-uma-chave-segura
# Obrigatório para rodar com banco real:
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DB?sslmode=require
```

**4. Banco de dados**

```bash
flask --app wsgi.py db upgrade
```

**5. Criar o administrador (painel /admin)**

```bash
python scripts/seed.py
```

Isso cria o usuário **ghlp** com senha **1234** na tabela `admins` (se ainda não existir). O login do painel admin em `/admin/login` usa essa tabela.

**6. Rodar o servidor**

```bash
flask --app wsgi.py run --debug
# ou, para usar a porta 5001: flask --app wsgi.py run --debug --port 5001
```

Acesse: http://127.0.0.1:5000 (ou a porta que o Flask indicar, ex.: 5001). Painel admin: http://127.0.0.1:5001/admin/login (usuário **ghlp**, senha **1234**, após rodar o seed).

## Contribuindo

Bugs e pull requests são bem-vindos em [github.com/gustavopinto/icse-accommodation](https://github.com/gustavopinto/icse-accommodation).
