run:
	uvicorn api:app --host 0.0.0.0 --port 5042 --reload --ws none

build:
	docker compose up --build -d

logs:
	docker compose logs -f
