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
- **SQLite** em desenvolvimento, **PostgreSQL** em produção

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
pip install -r requirements-dev.txt
```

**3. Variáveis de ambiente**

Crie um arquivo `.env` na raiz:

```env
FLASK_ENV=development
SECRET_KEY=troque-por-uma-chave-segura
# DATABASE_URL=sqlite:///app.db  ← padrão, pode omitir
```

**4. Banco de dados**

```bash
flask --app wsgi.py db upgrade
```

**5. Rodar o servidor**

```bash
flask --app wsgi.py run --debug
```

Acesse: http://127.0.0.1:5000

## Contribuindo

Bugs e pull requests são bem-vindos em [github.com/gustavopinto/icse-accommodation](https://github.com/gustavopinto/icse-accommodation).
