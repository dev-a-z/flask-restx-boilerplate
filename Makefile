.ONESHELL:

.PHONY: clean install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	pip install -r requirements.txt

tests:
	
	pytest

run:
	
	flask run --host 0.0.0.0

all: clean install tests run

routes: 
	flask routes

docker-build:
	docker build -f ./build/docker/Dockerfile . -t flask-restx-boilerplate

docker-run:
	docker-compose -f build/docker/docker-compose.yml up -d

docker-stop:
	docker-compose -f build/docker/docker-compose.yml down
