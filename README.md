# ICSE 2026 — Accommodation

A site for [ICSE 2026](https://conf.researchr.org/home/icse-2026) (Rio de Janeiro) attendees to find people interested in sharing accommodation.

> **This site has no official affiliation with the conference.** It is an individual initiative by [Gustavo Pinto](https://gustavopinto.org).

## Features

- Public listing of accommodation requests
- Registration form — no account needed, just a valid email
- Fields: name, email, institution, period (check-in/check-out), gender identity, roommate preference, smoker, social media, and personal website
- Social network icon automatically detected from the URL (LinkedIn, GitHub, Instagram, X, etc.)

## Stack

- **Python 3.11+** / **Flask 3**
- **Flask-SQLAlchemy** + **Flask-Migrate** (Alembic)
- **Flask-WTF** (forms with CSRF protection)
- **PostgreSQL** (e.g. [Neon](https://neon.tech)); SQLite for local testing only

## Local setup

**1. Clone and create virtual environment**

```bash
git clone https://github.com/gustavopinto/icse-accommodation.git
cd icse-accommodation
python -m venv .venv
source .venv/bin/activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
# or requirements-dev.txt for development
```

**3. Environment variables**

Copy `.env.example` to `.env` and fill in the values. **Never commit `.env`** (it contains credentials).

**4. Database**

```bash
flask --app wsgi.py db upgrade
```

**5. Run the server**

```bash
flask --app wsgi.py run --debug
```

Visit: http://127.0.0.1:5000 — Admin panel: `/admin/login`

## Contributing

Bugs and pull requests are welcome at [github.com/gustavopinto/icse-accommodation](https://github.com/gustavopinto/icse-accommodation).
