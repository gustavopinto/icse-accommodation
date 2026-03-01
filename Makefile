.PHONY: install run migrate seed test

install:
	python -m pip install -r requirements-dev.txt

run:
	flask --app wsgi.py run --debug

migrate:
	flask --app wsgi.py db init || true
	flask --app wsgi.py db migrate -m "$(m)"
	flask --app wsgi.py db upgrade

seed:
	python scripts/seed.py

test:
	pytest

coverage:
	pytest --cov=app --cov-report=html
