# Stadtklima Project

This repo features a frontend and backend to securely manage sensor data and installations from a web portal.

The `/backend` folder contains:

- **[`/backend/api`](./backend/api)**: A Django REST-API to share sensor data and metrics
- **[`/backend/connectors`](./backend/connectors)**: Scripts to periodically import data from our sensor network
- **[`/backend/compute`](./backend/compute)**: Scripts that process raw sensor data into useful metrics

## Installation

A lightweight dockerized environment is provided with the ability to bootstrap the entire application and run everything as intended. Either use this directly, or take a look at the `docker-compose.yml` file for a complete list of services needed for the execution environment of this product.

Snapshot of key services:

|                                                   | Version | EOL     |
| ------------------------------------------------- | ------- | ------- |
| [PostgreSQL](https://hub.docker.com/_/postgres)   | 17      | 2029-11 |
| [Python](https://hub.docker.com/_/python)         | 3.12    | 2028-10 |
| [Node](https://hub.docker.com/_/node)             | 22 LTS  | 2027-04 |
| [Django](https://www.djangoproject.com/download/) | 4.2 LTS | 2026-04 |

### Configure ENV variables

Secret keys and configurable variables for production and development contexts are set in a `.env` file outside of version control. Please copy the `.env.example` file and configure ALL missing fields.

Generate tokens and keys for the `.env` file:

```sh
# Once for SECRET_KEY, CONN_PASSWORD
gpg --gen-random 2 56 | base64

# Once for CONN_TOKEN (max len is 40 chars)
gpg --gen-random 2 30 | base64
```

## Backend

### Manual Setup

```sh
# Run the migrations
python manage.py migrate

# Seed Provider data
python manage.py seed

# And create a superuser for the admin panel
python manage.py createsuperuser --username admin --email admin@example.com
```

Run the server

```sh
python manage.py runserver 0.0.0.0:8000
```

<!-- python manage.py flush && python manage.py setup_auth && python manage.py seed -->

### Migrations

If you change the ORMS:

```sh
# Generate new migration files
python manage.py makemigrations api

# Check the migration SQL output in plain text (dry run)
python manage.py sqlmigrate api 0001  # change number

# Run the migrations
python manage.py migrate
```
