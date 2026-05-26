.PHONY: test lint run docker-up docker-down build helm-template terraform-fmt

APP_DIR=apps/resume-ai-api

test:
	cd $(APP_DIR) && pytest

lint:
	cd $(APP_DIR) && ruff check .

run:
	cd $(APP_DIR) && uvicorn resume_ai_api.main:app --reload --port 8000

build:
	docker build -t resume-ai-api:local $(APP_DIR)
	docker build -t resume-ai-web:local apps/resume-ai-web

docker-up:
	docker compose up --build

docker-down:
	docker compose down

helm-template:
	helm template resume-ai platform/helm/resume-ai --namespace resume-ai-staging -f platform/helm/resume-ai/values.yaml -f platform/helm/resume-ai/values-staging.yaml

terraform-fmt:
	terraform fmt -recursive infra/terraform
