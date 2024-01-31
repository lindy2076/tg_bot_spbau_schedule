ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif


args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). See Makefile file."
else
MESSAGE = "Done"
endif


APPLICATION_NAME = timetable_bot
TEST = poetry run python3 -m pytest --verbosity=2 --showlocals --log-level=DEBUG
CODE = $(APPLICATION_NAME) tests
DOCKER_RUN = docker run -p 8000:8000 -it --env-file .env $(APPLICATION_NAME)


env:  
	@$(eval SHELL:=/bin/bash)
	@cp .env.sample .env
	@echo "BOT_TOKEN=your_key" >> .env
	@echo "ADMIN_ID=your_id" >> .env

run:
	python3 -m timetable_bot

up:
	docker compose -f docker-compose.yml up -d --remove-orphans

build:
	docker compose -f docker-compose.yml up -d --remove-orphans --build

migrate:
	cd $(APPLICATION_NAME)/db && alembic upgrade $(args)

revision:
	cd $(APPLICATION_NAME)/db && alembic revision --autogenerate

down:
	docker compose down

flake:
	flake8 $(APPLICATION_NAME) --exclude "*/db/migrator/*, *responses.py, */config.py"

%::
	echo $(MESSAGE)
