.PHONY: prod

dev:
	docker compose -f docker-compose.dev.yaml up -d

prod:
	docker compose -f docker-compose.prod.yaml up -d --build

down:
	docker compose -f docker-compose.prod.yaml down

logs:
	docker compose -f docker-compose.prod.yaml logs -f --tail=20

