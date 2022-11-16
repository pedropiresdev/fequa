
init:
	python3 -m venv env

install:
	pip install --upgrade pip
	pip install wheel
	pip install -r requirements.txt --no-cache

pretty:
	isort app/**/*.py && \
	flake8 app/*

format:
	black app  --line-length=140 --exclude=app/view/templates

secure:
	bandit -r app/* -x tests

safe:
	safety check -r requirements.txt

clean:
	find app -name '*.pyc' -exec rm -rf {} \;
	rm -rf .tox
	rm -rf .pytest_cache
	rm -rf *.egg-info
	rm -rf .coverage

up:
	docker-compose up --build

run:
	uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload

nameko:
	nameko run --config app/config.yaml app.service

load:
	locust -f tests/load.py

test:
	pytest -vv

.PHONY: init
