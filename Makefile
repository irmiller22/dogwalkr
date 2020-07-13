APP_NAME = dogwalkr
MODE = dev

all: build init logs purge

build:
	docker build -f ./images/Dockerfile -t $(APP_NAME):$(MODE) .

init: build
	docker-compose up -d

logs:
	docker-compose logs -f --tail=25

purge:
	docker-compose down --volumes --remove-orphans

migration:
	docker-compose exec api alembic revision --autogenerate

.PHONY: build init logs purge
