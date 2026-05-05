# Thrust HRMS (Odoo 19)

Custom HR modules for Odoo 19 live under `addons19/`. This repository is meant to run with **Docker Compose**: PostgreSQL 15 plus an **Odoo 19** image built from this repo’s `Dockerfile` (adds `python3-pandas`, required by `ohrms_core`), with local addons mounted into the container.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) with Compose v2

## Quick start

From the repository root:

```bash
docker compose up -d
```

Open **http://127.0.0.1:8081** in your browser. Odoo listens on port **8069** inside the container; it is published as **8081** on the host to reduce clashes with other services.

## Database credentials (Compose)

These match `docker-compose.yml` and are used by the Odoo service to connect to PostgreSQL:

| Variable | Value |
|----------|--------|
| Host (inside Compose network) | `db` |
| User | `odoo` |
| Password | `odoo` |
| PostgreSQL database name | `postgres` (default cluster DB; **your Odoo company database** is created in the browser and has its own name) |

## First run

If no database exists yet, Odoo will prompt you to **create a database** and an administrator account. After login, install or enable the HR-related apps you need under **Apps**. You may need **Developer mode** (Settings) and **Update Apps List** to see custom modules from `addons19/`.

## Install every addon under `addons19/` (CLI)

Stop the web container so Odoo is not holding the database, then install all top-level modules that contain `__manifest__.py`. Replace `YourOdooDatabaseName` with your real database name (see `\l` in Postgres as in [Troubleshooting login](#troubleshooting-login)).

```bash
MODS=$(cd addons19 && for d in */; do [ -f "${d}__manifest__.py" ] && printf '%s,' "${d%/}"; done | sed 's/,$//')
docker compose stop web
docker compose run --rm web odoo -d YourOdooDatabaseName --db_host=db --db_user=odoo --db_password=odoo --stop-after-init -i "$MODS"
docker compose up -d web
```

Odoo resolves dependencies automatically. If one addon fails to install, fix the error shown in the log and run the command again (already-installed modules are skipped).

## Useful commands

```bash
# Start stack (detached)
docker compose up -d

# View logs (Odoo web service)
docker compose logs -f web

# Stop stack (containers stopped; named volumes kept)
docker compose down

# Stop and remove volumes (deletes DB and Odoo filestore — destructive)
docker compose down -v
```

## Running alongside other Odoo stacks

This project does **not** pin fixed `container_name` values, so Compose names services after the project (for example `thrust_hrms-web-1`). That avoids clashes when another Odoo project on the same machine uses different container names or ports.

## Troubleshooting login

- **Wrong email or password** — The login is the user’s **Login** field in Odoo (often an email), not the PostgreSQL password from the table above.
- **Many failed attempts** — Odoo 19 can temporarily block further attempts from your IP (rate limiting). Check `docker compose logs web` for messages about login cooldown.
- **Reset a user password (Docker)** — Replace `YourOdooDatabaseName` and run from the repo root (service name may differ; use `docker compose ps`):

```bash
docker exec -i thrust_hrms-web-1 odoo shell -d YourOdooDatabaseName --db_host=db --db_user=odoo --db_password=odoo <<'PY'
u = env['res.users'].search([('login', '=', 'you@example.com')], limit=1)
u.password = 'choose-a-new-password'
env.cr.commit()
print('Updated:', u.login)
PY
```

To list Odoo database names in Postgres: `docker exec thrust_hrms-db-1 psql -U odoo -d postgres -c '\l'`.

---

Port **8081** is configurable in `docker-compose.yml` under `services.web.ports` if you need to change it.
