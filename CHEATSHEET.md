# Cheatsheet

Overview of the most common commands.

## Installation

Install:
- Docker
- Conda
- docker-compose

```
docker-compose up -d --build
```

- BioSegment is now running in dev mode at localhost

## Overview
Dash-frontend, using Python Dash: http://localhost/dash

Frontend, built with Docker, with routes handled based on the path: http://localhost

Backend, JSON based web API based on OpenAPI: http://localhost/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc

PGAdmin, PostgreSQL web administration: http://localhost:5050

Flower, administration of Celery tasks: http://localhost:5555

Traefik UI, to see how the routes are being handled by the proxy: http://localhost:8090

## Development
- Dash frontend and backend hot-reload on file changes
- Database schema changes need the removal of the database volume

- Backend tests
```
docker-compose exec backend bash /app/tests-start.sh
```

- Backend linting and formatting
```
cd backend/app
poetry install
poetry shell
sh scripts/format.sh
sh scripts/format-imports.sh
sh scripts/lint.sh
```

## Run celery worker with GPU

- docker-compose GPU support is very experimental, not working currently
    - see `docker-compose_gpu.yml`
    - docker-compose override gives errors, that's why one .yml file is needed
    - NVIDIA driver still isn't visible then, waiting for stable support

Current workaround
- expose rabbitMQ queue in docker-compose to host
- run celery worker on host without virtualization
```
# in backend/app
# install environment for celery worker
conda env update -f ../celery_pytorch_environment.yaml
conda env update -f ../celery_celery_environment.yaml
conda env update -f ../celery_neuralnets_environment.yaml

# in gpu_worker
conda activate celery_neuralnets
celery worker -A app.worker -l info -Q main-queue -c 1
```