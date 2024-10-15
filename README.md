## Get it Running

Generate tokens and keys for the `.env` file:

```sh
# Once for SECRET_KEY, CONN_PASSWORD
gpg --gen-random 2 56 | base64

# Once for CONN_TOKEN (max len is 40 chars)
gpg --gen-random 2 30 | base64
```

Get database set up:

```sh
# Run the migrations
python manage.py migrate

# Seed data
python manage.py flush && python manage.py seed

# And create a superuser for the admin panel
python manage.py createsuperuser --username admin --email admin@example.com
```

Run the server

```sh
python manage.py runserver 0.0.0.0:8000
```

python manage.py flush && python manage.py setup_auth && python manage.py seed

## Migrations

If you change the ORMS:

```sh
# Generate new migration files
python manage.py makemigrations api

# Check the migration SQL output in plain text (dry run)
python manage.py sqlmigrate api 0001  # change number

# Run the migrations
python manage.py migrate
```
