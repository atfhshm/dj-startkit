.PHONEY: clean
clean:
	uv run pyclean .

.PHONEY: format
format:
    uv run ruff format

.PHONEY: dev
dev:
	uv run manage.py runserver

.PHONEY: gunicorn
gunicorn:
	uv run gunicorn --config gunicorn_config.py

.PHONEY: makemigrations
makemigrations:
	uv run manage.py makemigrations

.PHONEY: migrate
migrate: makemigrations
	uv run manage.py migrate

.PHONEY: superuser
superuser:
	uv run manage.py createsuperuser

app_name := $(app_name)

.PHONEY: create_app_dir
create_app_dir:
	mkdir apps/$(app_name) 

.PHONEY: create-app
create_app: create_app_dir
	uv run manage.py startapp $(app_name) apps/$(app_name)

.PHONEY: cov-report
cov-report:
	uv run pytest --cov=./apps --cov-report=html