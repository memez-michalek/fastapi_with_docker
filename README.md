![Continuous Integration and Delivery](https://github.com/memez-michalek/fastapi_with_docker/workflows/Continuous%20Integration%20and%20Delivery/badge.svg?branch=main)
# FastAPI with TDD and Docker

This project demonstrates how to use FastAPI, Test-Driven Development (TDD) and Docker together to create a web application.

## Getting Started

To get started, follow these steps:

1. Clone the repository:

git clone https://github.com/memez-michalek/fastapi_with_docker.git

2. Navigate to the project directory:

cd fastapi_with_docker

3. Build and run the Docker images with docker-compose:

docker-compose up -d --build

This will start the FastAPI application inside a Docker container using detached mode and expose it on port 8000.

4 Open your web browser and navigate to http://localhost:8000/docs

You'll see Swagger explanation of api endpoints


## Running Tests

This project uses Pytest for testing. To run the tests, first make sure that the Docker container is running, then run:

docker-compose exec fastapi python -m pytest


