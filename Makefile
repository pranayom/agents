test:
	python -m pytest

lint:
	python -m ruff check .

typecheck:
	python -m mypy .

format:
	python -m ruff format .
