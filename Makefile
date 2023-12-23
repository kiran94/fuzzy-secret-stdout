
test:
	poetry run pytest -x

coverage:
	poetry run pytest -q --cov=ssm_view --cov-report=term # for local
	poetry run pytest -q --cov=ssm_view --cov-report=html # for local

	# for sonarqube
	$(if $(GITHUB_ACTIONS),poetry run pytest -q --cov=ssm_view --cov-report=xml,)

	# for github action
	$(if $(GITHUB_ACTIONS),poetry run pytest -q --cov=ssm_view --cov-report=lcov,)

lint:
	poetry run ruff check $(if $(GITHUB_ACTIONS),--format github,) .

format:
	poetry run ruff check --fix .

run:
	poetry run python -m ssm_view
