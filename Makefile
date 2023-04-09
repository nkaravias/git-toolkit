
docker-build:
	docker-compose build

docker-run: docker-build
	docker-compose run local

install:
	pip install -r commit_analyser/requirements.txt
	pip install pytest pytest-cov

lint:
	python -m flake8

test:
	python -m pytest --cov --cov-report=html -v .

run:
	python git_utils.py -o yaml -f lala.yaml data/repo