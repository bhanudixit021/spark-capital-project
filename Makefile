#This makefile handles the common commands from the project
TAG := $$(git rev-parse --short HEAD)


run:
	uvicorn main:app --reload

docker-be:
	docker build -t spark-capital:$(TAG) -f Dockerfile.spark .

start-spark-capital:
	export TAG=${TAG} && docker-compose -f docker-compose.yml up -d --no-deps --build spark-capital


up:
	export TAG=${TAG} && docker-compose -f docker-compose.yml up -d
