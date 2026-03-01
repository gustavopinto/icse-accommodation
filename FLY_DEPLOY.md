# Deploy no Fly.io

Este projeto está configurado para rodar no [Fly.io](https://fly.io).

## Pré-requisitos

- Conta no [Fly.io](https://fly.io) (login com `fly auth login`)
- [flyctl](https://fly.io/docs/hub/cmd/flyctl/) instalado

## 1. Banco de dados (PostgreSQL)

O app usa **PostgreSQL** em produção. Você pode:

### Opção A: Postgres gerenciado pelo Fly

```bash
# Criar um cluster Postgres
fly postgres create --name icse-accomodation-db --region gru

# Anotar a connection string que aparecer (ou ver com):
fly postgres connect -a icse-accomodation-db
# No painel do app Postgres: Settings → Connection string

# Vincular ao app (injeta DATABASE_URL como secret)
fly postgres attach icse-accomodation-db -a icse-accomodation
```

### Opção B: Postgres externo (Neon, Supabase, etc.)

Defina o secret com a URL do banco:

```bash
fly secrets set DATABASE_URL="postgresql://user:password@host:5432/dbname" -a icse-accomodation
```

## 2. Secrets obrigatórios

```bash
# Chave secreta da aplicação (obrigatório em produção)
fly secrets set SECRET_KEY="uma-string-aleatoria-longa-e-segura" -a icse-accomodation
```

## 3. Primeiro deploy

```bash
# Na raiz do projeto
fly launch --no-deploy   # só cria o app; não faz deploy ainda

# Se o nome do app for diferente, edite app = "..." no fly.toml

# Defina os secrets (DATABASE_URL e SECRET_KEY) como acima, depois:
fly deploy
```

Se você já tiver rodado `fly launch` antes e o app já existir:

```bash
fly deploy
```

## 4. Comandos úteis

| Comando | Descrição |
|--------|-----------|
| `fly deploy` | Faz deploy da aplicação |
| `fly logs` | Ver logs em tempo real |
| `fly status` | Status do app e máquinas |
| `fly open` | Abre a URL do app no navegador |
| `fly ssh console` | Abre um shell no container |
| `fly secrets list` | Lista secrets configurados |

## 5. Região

No `fly.toml` está `primary_region = "gru"` (São Paulo). Para mudar:

```bash
fly regions set ams  # Amsterdam, por exemplo
```

E edite `primary_region` no `fly.toml` se quiser manter consistente.

## 6. Migrations

As migrations rodam automaticamente em cada deploy via `release_command` no `fly.toml`:

```toml
[deploy]
  release_command = "flask --app wsgi.py db upgrade"
```

Para criar novas migrations, faça localmente e faça commit da pasta `migrations/`:

```bash
flask --app wsgi.py db migrate -m "descrição da alteração"
```

Depois é só dar `fly deploy` de novo.
