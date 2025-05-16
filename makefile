
run_uvicorn:
	python3 src/run_uvicorn.py

postgres:
	docker run --name pg -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15-alpine

create_db:
	docker exec -it pg psql -U postgres -c "CREATE DATABASE pg;"
