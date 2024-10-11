Generate SECRET_KEY:

```sh
gpg --gen-random 2 70 | base64
```

## Migrations

```sh
# Generate new migration files if ORMs change
python manage.py makemigrations api

# Check the migration SQL output in plain text (dry run)
python manage.py sqlmigrate api 0001  # change number

# Run the migration
python manage.py migrate
```

## Development Server

```sh
python manage.py runserver 0.0.0.0:8000
```
