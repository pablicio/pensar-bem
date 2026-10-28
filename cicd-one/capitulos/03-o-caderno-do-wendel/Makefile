.PHONY: deps lint testes build

deps:
	pip install -r api/requirements.txt \
	  -r api/requirements-dev.txt

lint:
	ruff check api/ && ruff format --check api/

testes:
	pytest api/tests -q

build:
	docker build -t embarque-api:dev api/
