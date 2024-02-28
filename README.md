# Squint

###### Take a good look at all the ways you can lose money

### Getting Started

1. Copy `.env-example` to `.env`

```sh
cp .env-example .env
```

2. Start up Docker:

```sh
docker-compose up
```

3. View http://localhost:1999

### Development

1. Copy `.env-example` to `.env`

```sh
cp .env-example .env
```

2. Use VSCode and [VSCode Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Start it up in a Dev Container
4. cd into 'app' (from `/workspaces`):

```sh
cd app
```

5. Create the admin (see `app/home/management/commands/createsu.py`):

```sh
python manage.py createsu
```

6. (optional) make any db migration changes (if you're changing models.py anywhere; for example, `transactions`):

```sh
python manage.py makemigrations transactions
python manage.py migrate
```

7. Start the dev server:

```sh
python manage.py runserver 0.0.0.0:8000
```

8. (probably) navigate to http://localhost:1999 (see .env file for the default port)

### Tech

- Docker: https://www.docker.com/
- Django: https://www.djangoproject.com/
- VS Code: https://code.visualstudio.com/
- Playwright: https://playwright.dev/
- Express: https://expressjs.com/
- TBD
