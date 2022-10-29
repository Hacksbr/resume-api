build:
	@docker-compose build

bash:
	@docker-compose run --rm resume bash

run:
	@docker-compose up

test:
	@docker-compose run --rm resume bash -c 'pytest'

down:
	@docker-compose down -v

makemigrations:
	@poetry run ./manage.py makemigrations

migrate:
	@poetry run ./manage.py migrate

createsuperuser:
	@poetry run ./manage.py createsuperuser

local-test:
	@poetry run pytest
