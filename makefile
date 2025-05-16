
run_gunicorn:
	python3 src/run_gunicorn.py

run_uvicorn:
	python3 src/run_uvicorn.py

postgres:
	docker run --name pg -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15-alpine

db:
	docker exec -it pg psql -U postgres -c "CREATE DATABASE pg;"


run_redis:
	docker run --rm -d -p 6379:6379 --name dashboard_redis redis:alpine

