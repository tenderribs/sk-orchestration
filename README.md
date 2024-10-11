## Get it Running

Generate a `SECRET_KEY` for the `.env` file:

```sh
gpg --gen-random 2 70 | base64
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
