
test:
	poetry run pytest -x

coverage:
	poetry run pytest -q --cov=fuzzy_secret_stdout --cov-report=term # for local
	poetry run pytest -q --cov=fuzzy_secret_stdout --cov-report=html # for local

	# for sonarqube
	$(if $(GITHUB_ACTIONS),poetry run pytest -q --cov=fuzzy_secret_stdout --cov-report=xml,)

	# for github action
	$(if $(GITHUB_ACTIONS),poetry run pytest -q --cov=fuzzy_secret_stdout --cov-report=lcov,)

lint:
	poetry run ruff check $(if $(GITHUB_ACTIONS),--output-format github,) .

format:
	poetry run ruff check --fix .

run: run_ssm

run_ssm:
	poetry run python -m fuzzy_secret_stdout -i AWS_SSM

run_secretmanager:
	poetry run python -m fuzzy_secret_stdout -i AWS_SECRET_MAN | jq .
