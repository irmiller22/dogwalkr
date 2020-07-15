APP_NAME = dogwalkr
MODE = dev

all: build ddl_dump destroy init logs migration purge shell upgrade

build:
	docker build -f ./images/Dockerfile -t $(APP_NAME):$(MODE) .

ddl_dump:
	docker-compose exec db pg_dump -U $(APP_NAME) $(APP_NAME) --quote-all-identifiers --no-owner --no-privileges --no-acl --no-security-labels --schema-only | sed -e '/^--/d' > sql/$(APP_NAME).sql

destroy:
	docker-compose down --rmi all --volumes --remove-orphans

init: build
	docker-compose up -d

logs:
	docker-compose logs -f --tail=25

migration:
	docker-compose exec api alembic revision --autogenerate

purge:
	docker-compose down --volumes --remove-orphans

shell:
	docker-compose exec api /bin/bash

upgrade:
	docker-compose exec api alembic upgrade heads


.PHONY: build ddl_dump destroy init logs migration purge shell upgrade
