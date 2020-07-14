APP_NAME = dogwalkr
MODE = dev

all: build init logs purge

build:
	docker build -f ./images/Dockerfile -t $(APP_NAME):$(MODE) .

ddl_dump:
	docker-compose exec db pg_dump -U dogwalkr dogwalkr --quote-all-identifiers --no-owner --no-privileges --no-acl --no-security-labels --schema-only | sed -e '/^--/d' > sql/dogwalkr.sql

init: build
	docker-compose up -d

logs:
	docker-compose logs -f --tail=25

migration:
	docker-compose exec api alembic revision --autogenerate

purge:
	docker-compose down --volumes --remove-orphans


.PHONY: build init logs purge
